from typing import Any, Optional

import requests
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View

from user.models import CommonUser
from user.schemas import (
    KakaoLoginRequest,
    KakaoLoginResponse,
    NaverLoginRequest,
    NaverLoginResponse,
)
from user.views.views_token import create_access_token, create_refresh_token


def create_dummy_password(common_user):
    dummy_password = CommonUser.objects.make_random_password()
    common_user.set_password(dummy_password)
    common_user.save()
    return dummy_password


class KakaoLoginView(View):

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        try:
            print("요청된 카카오 인가 코드:", request.GET.get("code"))
            code = request.GET.get("code")
            if not code:
                print("Error: code가 없습니다.")  # 추가
                return JsonResponse(
                    {"message": "code가 필요합니다."}, status=400
                )

            kakao_access_token = self.get_kakao_access_token(code)
            print("카카오 액세스 토큰:", kakao_access_token)
            if not kakao_access_token:
                print("Error: 카카오 인증 실패")  # 추가
                return JsonResponse({"message": "카카오 인증 실패"}, status=400)

            user_data = self.get_kakao_user_info(kakao_access_token)
            print("카카오 사용자 데이터:", user_data)
            if not user_data:
                print("Error: 카카오 사용자 정보 요청 실패")  # 추가
                return JsonResponse(
                    {"message": "카카오 사용자 정보 요청 실패"}, status=400
                )

            email = user_data.get("kakao_account", {}).get("email")
            print("카카오 이메일:", email)
            common_user = self.get_or_create_common_user(email)

            if common_user:
                if hasattr(common_user, "userinfo"):
                    access_token = create_access_token(common_user)
                    refresh_token = create_refresh_token(common_user)
                    response = KakaoLoginResponse(
                        message="로그인 성공",
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type="bearer",
                    )
                    print("로그인 성공:", response.model_dump())  # 추가
                    return JsonResponse(response.model_dump(), status=200)

                print("추가 정보 입력 필요:", email)  # 추가
                return JsonResponse(
                    {
                        "message": "추가 정보 입력 필요",
                        "email": email,
                    },
                    status=202,
                )

            print("Error: 사용자 생성 실패")  # 추가
            return JsonResponse({"message": "사용자 생성 실패"}, status=400)

        except Exception as e:
            print("Error 발생:", str(e))  # 추가
            return JsonResponse(
                {"message": "서버 오류", "error": str(e)}, status=500
            )

    def get_kakao_access_token(self, code: str) -> Optional[str]:
        """카카오 액세스 토큰을 발급받는 메서드"""
        kakao_token_url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_CLIENT_ID,
            "client_secret": settings.KAKAO_SECRET,
            "redirect_uri": settings.KAKAO_REDIRECT_URL,
            "code": code,
        }
        response = requests.post(kakao_token_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    def get_kakao_user_info(
        self, kakao_access_token: str
    ) -> Optional[dict[str, Any]]:
        """카카오 액세스 토큰으로 사용자 정보를 가져오는 메서드"""
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {kakao_access_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return None

    def get_or_create_common_user(self, email: str) -> Optional[CommonUser]:
        """이메일로 기존 사용자 조회 및 없다면 생성하는 메서드"""
        common_user = CommonUser.objects.filter(email=email).first()
        if not common_user:
            # 커먼유저가 존재하지 않으면 새로 생성하고 더미 비밀번호 추가
            common_user = CommonUser.objects.create(
                email=email,
                join_type="user",  # 기본 사용자 설정
                is_active=True,
            )
            create_dummy_password(common_user)  # 더미 비밀번호 생성
        return common_user


class NaverLoginView(View):
    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        try:
            code = request.GET.get("code")
            state = request.GET.get("state")
            if not code or not state:
                return JsonResponse(
                    {"message": "code와 state가 필요합니다."}, status=400
                )

            naver_access_token = self.get_naver_access_token(code, state)
            if not naver_access_token:
                return JsonResponse({"message": "네이버 인증 실패"}, status=400)

            user_data = self.get_naver_user_info(naver_access_token)
            if not user_data:
                return JsonResponse(
                    {"message": "네이버 사용자 정보 요청 실패"}, status=400
                )

            email = user_data.get("response", {}).get("email")
            common_user = self.get_or_create_common_user(email)

            if common_user:
                if hasattr(common_user, "userinfo"):
                    access_token = create_access_token(common_user)
                    refresh_token = create_refresh_token(common_user)
                    response = NaverLoginResponse(
                        message="로그인 성공",
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_type="bearer",
                    )
                    return JsonResponse(response.model_dump(), status=200)

                return JsonResponse(
                    {
                        "message": "추가 정보 입력 필요",
                        "email": email,
                    },
                    status=202,
                )

            return JsonResponse({"message": "사용자 생성 실패"}, status=400)

        except Exception as e:
            return JsonResponse(
                {"message": "서버 오류", "error": str(e)}, status=500
            )

    def get_naver_access_token(self, code: str, state: str) -> Optional[str]:
        url = "https://nid.naver.com/oauth2.0/token"
        params = {
            "grant_type": "authorization_code",
            "client_id": settings.NAVER_CLIENT_ID,
            "client_secret": settings.NAVER_SECRET,
            "code": code,
            "state": state,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    def get_naver_user_info(
        self, access_token: str
    ) -> Optional[dict[str, Any]]:
        url = "https://openapi.naver.com/v1/nid/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def get_or_create_common_user(self, email: str) -> Optional[CommonUser]:
        common_user = CommonUser.objects.filter(email=email).first()
        if not common_user:
            common_user = CommonUser.objects.create(
                email=email,
                join_type="user",
                is_active=True,
            )
            create_dummy_password(common_user)
        return common_user
