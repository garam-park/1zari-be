from typing import List, Optional, Set
from uuid import UUID

from django.contrib.gis.measure import D
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views import View
from pydantic import ValidationError

from job_posting.models import JobPosting, JobPostingBookmark
from search.models import District
from search.schemas import (
    JobPostingResultModel,
    JobPostingSearchQueryModel,
    JobPostingSearchResponseModel,
)
from utils.common import get_valid_normal_user


class SearchView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        token = request.user
        user = get_valid_normal_user(token)

        try:
            query = JobPostingSearchQueryModel(
                city=request.GET.getlist("city"),
                district=request.GET.getlist("district"),
                town=request.GET.getlist("town"),
                work_day=request.GET.getlist("work_day"),
                posting_type=request.GET.getlist("posting_type"),
                employment_type=request.GET.getlist("employment_type"),
                education=request.GET.get("education", ""),
                search=request.GET.get("search", ""),
            )
        except ValidationError as e:
            return JsonResponse({"errors": e.errors()}, status=400)

        qs = JobPosting.objects.all()
        if query.city:
            qs = qs.filter(city__in=query.city)
        if query.district:
            qs = qs.filter(district__in=query.district)
        if query.town:
            qs = qs.filter(town__in=query.town)
        if query.work_day:
            qs = qs.filter(work_day__overlap=query.work_day)
        if query.posting_type:
            qs = qs.filter(posting_type__in=query.posting_type)
        if query.employment_type:
            qs = qs.filter(employment_type__in=query.employment_type)
        if query.education:
            qs = qs.filter(education__in=query.education)

        if query.search:
            qs = qs.filter(
                Q(job_posting_title__icontains=query.search)
                | Q(summary__icontains=query.search)
                | Q(company_id__company_name__icontains=query.search)
            )

        region_qs = District.objects.filter(
            city_name__in=query.city,
            district_name__in=query.district,
            emd_name__in=query.town,
        )

        if not region_qs.exists():
            return JsonResponse(
                {"results": [], "error": "지역 정보를 찾을 수 없습니다."},
                status=404,
            )

        job_posting_ids: Set[UUID] = set()
        for region in region_qs:
            center_point = region.geometry.centroid
            nearby_qs = qs.filter(
                location__distance_lte=(center_point, D(km=3))
            )
            job_posting_ids.update(
                nearby_qs.values_list("job_posting_id", flat=True)
            )

        final_qs = JobPosting.objects.filter(job_posting_id__in=job_posting_ids)

        results = [
            JobPostingResultModel(
                job_posting_id=jp.job_posting_id,
                job_posting_title=jp.job_posting_title,
                city=jp.city,
                district=jp.district,
                is_bookmarked=(
                    JobPostingBookmark.objects.filter(
                        job_posting=jp, user=user.common_user
                    ).exists()
                    if user
                    else False
                ),
                deadline=jp.deadline,
            )
            for jp in final_qs
        ]

        response = JobPostingSearchResponseModel(results=results)
        return JsonResponse(response.model_dump(), status=200)
