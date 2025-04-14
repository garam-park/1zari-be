from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field,ConfigDict

# ------------------------
# Career (경력 정보)
# ------------------------


class CareerInfoBaseModel(BaseModel):
    company_name: str
    position: str
    employment_period_start: date
    employment_period_end: Optional[date] = None

    class Config:
        json_encoders = {date: lambda v: v.strftime("%Y-%m-%d")}


class CareerInfoCreateModel(CareerInfoBaseModel):
    pass


class CareerInfoModel(CareerInfoBaseModel):
    pass


# ------------------------
# Resume (이력서)
# ------------------------


class ResumeBaseModel(BaseModel):
    education: str
    introduce: str
    career_list: List[CareerInfoCreateModel] = Field(default_factory=list)


class ResumeCreateModel(ResumeBaseModel):
    pass


class ResumeUpdateModel(BaseModel):
    education: Optional[str] = None
    introduce: Optional[str] = None
    career_list: Optional[List[CareerInfoCreateModel]] = None


class ResumeModel(ResumeBaseModel):
    model_config = ConfigDict(from_attributes=True)
    resume_id: UUID
    career_list: List[CareerInfoModel]

# ------------------------
# 응답 모델
# ------------------------


class ResumeResponseModel(BaseModel):
    message: str
    resume: ResumeModel


class ResumeListResponseModel(BaseModel):
    message: str
    resume_list: List[ResumeModel]
