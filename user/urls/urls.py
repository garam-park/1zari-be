from django.urls.conf import path

from user.views.views import (
    CommonUserCreateView,
    CompanyInfoUpdateView,
    CompanyLoginView,
    CompanySignupView,
    LogoutView,
    UserDeleteView,
    UserInfoUpdateView,
    UserLoginView,
    UserSignupView,
    find_company_email,
    find_user_email,
    reset_company_password,
    reset_user_password,
)
from user.views.views_oauth import KakaoLoginView, NaverLoginView
from user.views.views_token import TokenRefreshView
from user.views.views_verify import (
    SendVerificationCodeView,
    VerifyBusinessRegistrationView,
    VerifyCodeView,
)

app_name = "user"


urlpatterns = [
    path(
        "common_user/signup/",
        CommonUserCreateView.as_view(),
        name="common_signup",
    ),
    path("signup/", UserSignupView.as_view(), name="user-signup"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("company/signup/", CompanySignupView.as_view(), name="company-signup"),
    path("company/login/", CompanyLoginView.as_view(), name="company-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "verify/send-code/",
        SendVerificationCodeView.as_view(),
        name="send-verification-code",
    ),
    path("verify/code/", VerifyCodeView.as_view(), name="verify-code"),
    path(
        "verify/business/",
        VerifyBusinessRegistrationView.as_view(),
        name="verify-business",
    ),
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao-login"),
    path("naver/login/", NaverLoginView.as_view(), name="naver-login"),
    path("find//email/", find_user_email, name="find-user-email"),
    path("find/company/email/", find_company_email, name="find-company-email"),
    path("reset/password/", reset_user_password, name="reset-user-password"),
    path(
        "reset/company/password/",
        reset_company_password,
        name="reset-company-password",
    ),
    path("info/", UserInfoUpdateView.as_view(), name="user-info-update"),
    path(
        "company/info/",
        CompanyInfoUpdateView.as_view(),
        name="company-info-update",
    ),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
]
