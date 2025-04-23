import json
from datetime import datetime, timedelta

import jwt
import pytest
from django.conf import settings
from django.test import Client

from user.models import CommonUser, CompanyInfo, UserInfo
from user.views.views_token import create_refresh_token


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def common_user_data():
    return {
        "email": "test_user@example.com",
        "password": "testpassword123!",
        "join_type": "user",
        "is_active": True,
    }


@pytest.fixture
def common_company_data():
    return {
        "email": "test_company@example.com",
        "password": "testpassword123!",
        "join_type": "company",
        "is_active": True,
    }


@pytest.mark.django_db
def test_common_user_create(client, common_user_data):
    response = client.post(
        "/api/user/common_user/signup/",
        data=json.dumps(common_user_data),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert CommonUser.objects.filter(email=common_user_data["email"]).exists()


@pytest.mark.django_db
def test_user_signup(client, common_user_data):
    # 공통 유저 생성
    common_user = CommonUser.objects.create_user(**common_user_data)

    user_signup_data = {
        "common_user_id": str(common_user.common_user_id),
        "name": "홍길동",
        "phone_number": "01012345678",
        "gender": "male",
        "birthday": "1990-01-01",
        "interest": ["AI", "Web"],
        "purpose_subscription": ["job_search"],
        "route": ["friend"],
    }

    response = client.post(
        "/api/user/signup/",
        data=json.dumps(user_signup_data),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert UserInfo.objects.filter(common_user=common_user).exists()


@pytest.mark.django_db
def test_company_signup(client, common_company_data):
    common_user = CommonUser.objects.create_user(**common_company_data)

    company_signup_data = {
        "common_user_id": str(common_user.common_user_id),
        "company_name": "테스트 회사",
        "establishment": "2020-01-01",
        "company_address": "서울시 강남구",
        "business_registration_number": "123-45-67890",
        "company_introduction": "우리는 IT 기업입니다.",
        "company_logo": None,
        "certificate_image": "image_url",
        "ceo_name": "김대표",
        "manager_name": "김대표",
        "manager_phone_number": "01087654321",
        "manager_email": "corp@example.com",
        "is_staff": True,
    }

    response = client.post(
        "/api/user/company/signup/",
        data=json.dumps(company_signup_data),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert CompanyInfo.objects.filter(common_user=common_user).exists()


@pytest.mark.django_db
def test_user_login(client, common_user_data):
    CommonUser.objects.create_user(**common_user_data)

    login_data = {
        "email": common_user_data["email"],
        "password": common_user_data["password"],
        "is_active": common_user_data["is_active"],
    }

    response = client.post(
        "/api/user/login/",
        data=json.dumps(login_data),
        content_type="application/json",
    )

    # 응답 로그 추가
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.django_db
def test_company_login(client, common_company_data):
    CommonUser.objects.create_user(**common_company_data)

    login_data = {
        "email": common_company_data["email"],
        "password": common_company_data["password"],
        "is_active": common_company_data["is_active"],
    }

    response = client.post(
        "/api/user/company/login/",
        data=json.dumps(login_data),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.django_db
def test_logout_view(client, common_user_data):
    user = CommonUser.objects.create_user(**common_user_data)
    refresh_token = create_refresh_token(user)

    response = client.post(
        "/api/user/logout/",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )

    print(f"JSON: {response.json()}")

    assert response.status_code == 200
    assert response.json()["message"] == "로그아웃 성공"
