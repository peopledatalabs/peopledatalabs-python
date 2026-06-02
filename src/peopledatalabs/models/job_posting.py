"""
Models for input parameters of the Job Posting APIs.
"""

from datetime import date
from enum import Enum

from typing import Annotated

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
    size: Annotated[int, Field(ge=1, le=100)] | None = 10
    pretty: bool | None = False
    scroll_token: str | None = None


class JobPostingParamSearchModel(BaseModel):
    """
    Validator model for the job_posting search API when using the field-based
    parameter form (no 'query' body).
    """

    id: str | None = None
    first_seen_min: date | None = None
    first_seen_max: date | None = None
    deactivated_date_min: date | None = None
    deactivated_date_max: date | None = None

    title: str | None = None
    title_class: str | None = None
    title_role: str | None = None
    title_sub_role: str | None = None
    title_levels: str | None = None

    company_id: str | None = None
    company_name: str | None = None
    company_industry: str | None = None
    company_industry_v2: str | None = None
    company_website: str | None = None
    company_profile: str | None = None

    location: str | None = None
    description: str | None = None

    salary_range_min: int | None = None
    salary_range_max: int | None = None
    salary_currency: str | None = None
    salary_period: SalaryPeriod | None = None

    remote_work_policy: RemoteWorkPolicy | None = None
    inferred_skills: str | None = None
    last_verified_min: date | None = None
    last_verified_max: date | None = None

    is_active: bool | None = None
    size: Annotated[int, Field(ge=1, le=100)] | None = 10
    pretty: bool | None = False
    scroll_token: str | None = None
