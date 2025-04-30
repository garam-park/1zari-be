from datetime import date
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class JobPostingResultModel(BaseModel):
    job_posting_id: UUID
    job_posting_title: str
    city: str
    district: str
    is_bookmarked: bool
    deadline: date


class JobPostingSearchQueryModel(BaseModel):
    city: Optional[List[str]] = None
    district: Optional[List[str]] = None
    town: Optional[List[str]] = None
    work_day: Optional[List[str]] = None
    posting_type: Optional[List[str]] = None
    employment_type: Optional[List[str]] = None
    education: Optional[str] = None
    search: Optional[str] = None


class JobPostingSearchResponseModel(BaseModel):
    results: List[JobPostingResultModel]


class RegionTreeResponse(BaseModel):
    """
    지역 계층 구조 응답 모델
    """

    __root__: Dict[str, Dict[str, List[str]]]
