"""
Models for input parameters of the Job Posting APIs.
"""

from datetime import date
from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class RemoteWorkPolicy(str, Enum):
    """
    Valid values for 'remote_work_policy' on job_posting search.
    """

    remote = "remote"
    onsite = "onsite"


class SalaryPeriod(str, Enum):
    """
    Valid values for 'salary_period' on job_posting search.
    """

    year = "year"
    month = "month"
    week = "week"
    day = "day"
    hour = "hour"


class JobPostingQuerySearchModel(BaseModel):
    """
    Validator model for the job_posting search API when using an Elasticsearch-
    style query body.
    """

    query: dict
    size: Optional[Annotated[int, Field(ge=1, le=100)]] = 10
    pretty: Optional[bool] = False
    scroll_token: Optional[str] = None


class JobPostingParamSearchModel(BaseModel):
    """
    Validator model for the job_posting search API when using the field-based
    parameter form (no 'query' body).
    """

    id: Optional[str] = None
    first_seen_min: Optional[date] = None
    first_seen_max: Optional[date] = None
    deactivated_date_min: Optional[date] = None
    deactivated_date_max: Optional[date] = None

    title: Optional[str] = None
    title_class: Optional[str] = None
    title_role: Optional[str] = None
    title_sub_role: Optional[str] = None
    title_levels: Optional[str] = None

    company_id: Optional[str] = None
    company_name: Optional[str] = None
    company_industry: Optional[str] = None
    company_industry_v2: Optional[str] = None
    company_website: Optional[str] = None
    company_profile: Optional[str] = None

    location: Optional[str] = None
    description: Optional[str] = None

    salary_range_min: Optional[int] = None
    salary_range_max: Optional[int] = None
    salary_currency: Optional[str] = None
    salary_period: Optional[SalaryPeriod] = None

    remote_work_policy: Optional[RemoteWorkPolicy] = None
    inferred_skills: Optional[str] = None
    last_verified_min: Optional[date] = None
    last_verified_max: Optional[date] = None

    is_active: Optional[bool] = None
    size: Optional[Annotated[int, Field(ge=1, le=100)]] = 10
    pretty: Optional[bool] = False
    scroll_token: Optional[str] = None
