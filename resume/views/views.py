import json
import uuid
from typing import List

from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from resume.models import CareerInfo, Resume
from resume.schemas import (
    CareerInfoModel,
    ResumeCreateModel,
    ResumeListResponseModel,
    ResumeModel,
    ResumeResponseModel,
    ResumeUpdateModel,
)


def serialize_careers(careers: List[CareerInfo]) -> List[CareerInfoModel]:
    return [
        CareerInfoModel(
            company_name=career.company_name,
            position=career.position,
            employment_period_start=career.employment_period_start,
            employment_period_end=career.employment_period_end,
        )
        for career in careers
    ]


@method_decorator(csrf_protect, name="dispatch")
class MyResumeListView(View):
    """
    내 이력서 리스트 확인
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            user_id: uuid.UUID = request.user.id
            resumes = Resume.objects.filter(user_id=user_id).prefetch_related(
                "careers"
            )

            resume_models: List[ResumeModel] = []
            for resume in resumes:
                careers = serialize_careers(resume.careers.all())
                resume_models.append(
                    ResumeModel(
                        resume_id=resume.resume_id,
                        education=resume.education,
                        introduce=resume.introduce,
                        career_list=careers,
                    )
                )

            response = ResumeListResponseModel(
                message="Resume list loaded successfully",
                resume_list=resume_models,
            )
            return JsonResponse(response.model_dump(), status=200)
        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)


@method_decorator(csrf_protect, name="dispatch")
class MyResumeDetailView(View):
    """
    이력서 단일 조회 / 생성 / 수정 / 삭제
    """

    def get(self, request: HttpRequest, resume_id: uuid.UUID) -> HttpResponse:
        try:
            user = request.user
            resume = (
                Resume.objects.filter(user_id=user, resume_id=resume_id)
                .prefetch_related("careers")
                .first()
            )
            if not resume:
                return JsonResponse({"error": "Resume not found"}, status=404)

            career_models = serialize_careers(resume.careers.all())
            resume_model = ResumeModel(
                resume_id=resume.resume_id,
                education=resume.education,
                introduce=resume.introduce,
                career_list=career_models,
            )
            response = ResumeResponseModel(
                message="Resume loaded successfully", resume=resume_model
            )
            return JsonResponse(response.model_dump(), status=200)
        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        새로운 이력서 등록
        """
        try:
            data = json.loads(request.body)
            resume_data = ResumeCreateModel(**data)
            user = request.user

            with transaction.atomic():
                new_resume = Resume.objects.create(
                    user_id=user,
                    education=resume_data.education,
                    introduce=resume_data.introduce,
                )

                for career in resume_data.career_list:
                    CareerInfo.objects.create(
                        resume=new_resume,
                        company_name=career.company_name,
                        position=career.position,
                        employment_period_start=career.employment_period_start,
                        employment_period_end=career.employment_period_end,
                    )

                career_models = serialize_careers(new_resume.careers.all())
                resume_model = ResumeModel(
                    resume_id=new_resume.resume_id,
                    education=new_resume.education,
                    introduce=new_resume.introduce,
                    career_list=career_models,
                )
                response = ResumeResponseModel(
                    message="Resume created successfully", resume=resume_model
                )
                return JsonResponse(response.model_dump(), status=201)

        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)

    def patch(self, request: HttpRequest, resume_id: uuid.UUID) -> HttpResponse:
        """
        이력서 수정
        """
        try:
            data = json.loads(request.body)
            update_data = ResumeUpdateModel(**data)
            user = request.user

            resume = (
                Resume.objects.filter(user_id=user, resume_id=resume_id)
                .prefetch_related("careers")
                .first()
            )
            if not resume:
                return JsonResponse({"error": "Resume not found"}, status=404)

            # 기본 정보 수정
            if update_data.education is not None:
                resume.education = update_data.education
            if update_data.introduce is not None:
                resume.introduce = update_data.introduce
            resume.save()

            # 경력 수정
            if update_data.career_list is not None:
                resume.careers.all().delete()
                for career in update_data.career_list:
                    CareerInfo.objects.create(
                        resume=resume,
                        company_name=career.company_name,
                        position=career.position,
                        employment_period_start=career.employment_period_start,
                        employment_period_end=career.employment_period_end,
                    )

            career_models = serialize_careers(resume.careers.all())
            resume_model = ResumeModel(
                resume_id=resume.resume_id,
                education=resume.education,
                introduce=resume.introduce,
                career_list=career_models,
            )
            response = ResumeResponseModel(
                message="Resume updated successfully", resume=resume_model
            )
            return JsonResponse(response.model_dump(), status=200)

        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)

    def delete(
        self, request: HttpRequest, resume_id: uuid.UUID
    ) -> HttpResponse:
        """
        이력서 삭제
        """
        try:
            user = request.user
            resume = Resume.objects.get(user_id=user, resume_id=resume_id)
            resume.delete()
            return JsonResponse(
                {"message": "Successfully deleted resume"}, status=200
            )
        except Resume.DoesNotExist:
            return JsonResponse({"error": "Resume not found"}, status=404)
        except Exception as e:
            return JsonResponse({"errors": str(e)}, status=400)
