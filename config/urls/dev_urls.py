from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/resume/", include("resume.urls.resume_urls")),
    path("api/submission/", include("resume.urls.submission_urls")),
    path("api/job-postings/", include("job_posting.urls.urls")),
]
