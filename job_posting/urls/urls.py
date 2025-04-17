from django.urls import path

from job_posting.views.views import (
    JobPostingBookmarkView,
    JobPostingDetailView,
    JobPostingListView,
)

app_name = "job_posting"

urlpatterns = [
    # 공고 리스트 조회
    path("", JobPostingListView.as_view(), name="list"),
    # 공고 상세 조회 / 생성 / 수정 / 삭제
    path(
        "<uuid:job_posting_id>/", JobPostingDetailView.as_view(), name="detail"
    ),
    # 북마크 등록 / 삭제
    path(
        "<uuid:job_posting_id>/bookmark/",
        JobPostingBookmarkView.as_view(),
        name="bookmark",
    ),
    # 북마크 목록 조회
    path("bookmarks/", JobPostingBookmarkView.as_view(), name="bookmark_list"),
]
