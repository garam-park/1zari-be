from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from utils.schemas import MY_CONFIG

# ------------------------
# 공통 유저 (CommonUser)
# ------------------------


class CommonUserBaseModel(BaseModel):
    model_config = MY_CONFIG

    email: EmailStr
    join_type: str
    password: str


class CommonUserResponseModel(BaseModel):
    common_user_id: UUID
    email: EmailStr
    join_type: str
    last_login: Optional[str] = None  # 로그인 시간도 예시로 추가
    is_active: bool = False

    class Config:
        orm_mode = True


# ------------------------
# 일반 유저 가입 요청 모델
# ------------------------


class UserSignupRequest(BaseModel):
    model_config = MY_CONFIG

    common_user_id: UUID
    name: str
    phone_number: str
    gender: str
    birthday: Optional[date] = None
    interest: List[str] = Field(default_factory=list)
    purpose_subscription: List[str] = Field(default_factory=list)
    route: List[str] = Field(default_factory=list)


# ------------------------
# 일반 유저 (UserInfo)
# ------------------------


class UserInfoBaseModel(BaseModel):
    model_config = MY_CONFIG

    name: str
    phone_number: str
    gender: str
    birthday: Optional[date] = None
    interest: List[str] = Field(default_factory=list)
    purpose_subscription: List[str] = Field(default_factory=list)
    route: List[str] = Field(default_factory=list)


class UserInfoModel(BaseModel):
    model_config = MY_CONFIG

    user_id: UUID
    name: str
    phone_number: str
    gender: str
    birthday: Optional[date] = None
    interest: List[str] = Field(default_factory=list)
    purpose_subscription: List[str] = Field(default_factory=list)
    route: List[str] = Field(default_factory=list)


# ------------------------
# 기업 유저 가입 요청 모델
# ------------------------


class CompanySignupRequest(BaseModel):
    model_config = MY_CONFIG

    common_user_id: UUID
    company_name: str
    establishment: date
    company_address: str
    business_registration_number: str
    company_introduction: str
    certificate_image: str
    company_logo: Optional[str] = None
    ceo_name: str
    manager_name: str
    manager_phone_number: str
    manager_email: EmailStr
    is_staff: bool


# ------------------------
# 기업 유저 (CompanyInfo)
# ------------------------


class CompanyInfoBaseModel(BaseModel):
    model_config = MY_CONFIG

    company_name: str
    establishment: date
    company_address: str
    business_registration_number: str
    company_introduction: str
    certificate_image: str
    company_logo: Optional[str] = None
    ceo_name: str
    manager_name: str
    manager_phone_number: str
    manager_email: EmailStr
    is_staff: bool


class CompanyInfoModel(BaseModel):
    company_id: UUID
    company_name: str
    establishment: date
    company_address: str
    business_registration_number: str
    company_introduction: str
    certificate_image: str
    company_logo: Optional[str] = None
    ceo_name: str
    manager_name: str
    manager_phone_number: str
    manager_email: EmailStr
    is_staff: bool


# ------------------------
# 응답 모델
# ------------------------


class UserJoinResponseModel(BaseModel):
    model_config = MY_CONFIG

    message: str
    common_user: CommonUserResponseModel
    user_info: Optional[UserInfoModel] = None


class CompanyJoinResponseModel(BaseModel):
    model_config = MY_CONFIG

    message: str
    common_user: CommonUserResponseModel
    company_info: Optional[CompanyInfoModel] = None


# ------------------------
# 로그인 모델
# ------------------------


class UserLoginRequest(BaseModel):
    model_config = MY_CONFIG

    email: EmailStr
    password: str


class CompanyLoginRequest(BaseModel):
    model_config = MY_CONFIG

    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    model_config = MY_CONFIG

    message: str
    access_token: str
    refresh_token: str
    token_type: str


class CompanyLoginResponse(BaseModel):
    model_config = MY_CONFIG

    message: str
    access_token: str
    refresh_token: str
    token_type: str


# ------------------------
# 로그아웃 요청 모델
# ------------------------


class LogoutRequest(BaseModel):
    model_config = MY_CONFIG

    refresh_token: str


# ------------------------
# 토큰 갱신 모델
# ------------------------


class TokenRefreshRequest(BaseModel):
    model_config = MY_CONFIG

    refresh_token: str


class TokenRefreshResponse(BaseModel):
    model_config = MY_CONFIG

    access_token: str
    token_type: str


# ------------------------
# 토큰 검증 모델
# ------------------------


class TokenVerificationResponse(BaseModel):
    model_config = MY_CONFIG

    valid: bool
    message: str


# ------------------------
# 문자 인증 모델
# ------------------------


class SendVerificationCodeRequest(BaseModel):
    model_config = MY_CONFIG

    phone_number: str


class VerifyCodeRequest(BaseModel):
    model_config = MY_CONFIG

    phone_number: str
    code: str


# ------------------------
# 사업자등록번호 검증 모델
# ------------------------


class VerifyBusinessRegistrationRequest(BaseModel):
    model_config = MY_CONFIG

    b_no: str  # 사업자등록번호
    p_nm: str  # 대표자 이름
    start_dt: str  # 개업일자
