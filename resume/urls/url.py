from django.urls.conf import path

from resume.views.views import MyResumeDetailView, MyResumeListView

app_name = "resume"


urlpatterns = [
    path("", MyResumeListView.as_view(), name="resume"),
    path("<uuid:resume>/", MyResumeDetailView.as_view(), name="resume_detail"),
]
