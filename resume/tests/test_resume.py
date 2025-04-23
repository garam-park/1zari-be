import json

import pytest
from django.test.client import RequestFactory

from resume.models import Resume
from user.models import CommonUser, UserInfo


@pytest.fixture
def mock_common_user(db):
    user: CommonUser = CommonUser.objects.create(
        email="test@test.com",
        password="1q2w3e4r",
        join_type="nomal",
        is_active=True,
    )
    return user


@pytest.fixture
def mock_user(db, mock_common_user):
    user_info: UserInfo = UserInfo.objects.create(
        common_user=mock_common_user,
        name="test_name",
        phone_number="010123123",
        gender="male",
        interest=[],
        purpose_subscription=[],
        route=[],
    )
    return user_info


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.mark.django_db
def test_my_resume_list_view_get(factory, mock_user, mock_common_user):
    from resume.views.resume_views import MyResumeListView

    # 이력서 샘플 생성
    resume = Resume.objects.create(
        user=mock_user,
        resume_title="Test Resume",
        job_category="IT",
        education_level="Bachelor",
        school_name="Test University",
        education_state="Graduated",
        introduce="Test introduction",
    )

    request = factory.get("api/resume/")
    request.user = mock_common_user

    response = MyResumeListView.as_view()(request)
    print(response.content)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "resume_list" in data
    assert len(data["resume_list"]) >= 1
