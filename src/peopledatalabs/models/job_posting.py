"""
Models for input parameters of the Job Posting APIs.
"""

import base64
import json
from datetime import date
from enum import Enum
from typing import Any, List, Optional

from pydantic.v1 import (
    BaseModel,
    conint,
    validator,
)


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


def _parse_scroll_token(v):
    """
    Accepts either a decoded list or a base64-url-encoded JSON string and
    normalizes to a list. Mirrors the server-side scroll_token decoding.
    """
    if isinstance(v, str):
        json_str = base64.urlsafe_b64decode(v.encode()).decode()
        v = json.loads(json_str)
    return v


class JobPostingQuerySearchModel(BaseModel):
    """
    Validator model for the job_posting search API when using an
    Elasticsearch-style query body.
    """

    query: dict
    size: Optional[conint(le=100)] = 10
    pretty: Optional[bool] = False
    scroll_token: Optional[List[Any]] = None

    _parse_scroll_token = validator(
        "scroll_token", pre=True, allow_reuse=True
    )(_parse_scroll_token)


class JobPostingParamSearchModel(BaseModel):
    """
    Validator model for the job_posting search API when using the
    field-based parameter form (no 'query' body).
    """

    id: Optional[str]
    first_seen_min: Optional[date]
    first_seen_max: Optional[date]
    deactivated_date_min: Optional[date]
    deactivated_date_max: Optional[date]

    title: Optional[str]
    title_class: Optional[str]
    title_role: Optional[str]
    title_sub_role: Optional[str]
    title_levels: Optional[str]

    company_id: Optional[str]
    company_name: Optional[str]
    company_industry: Optional[str]
    company_industry_v2: Optional[str]
    company_website: Optional[str]
    company_profile: Optional[str]

    location: Optional[str]
    description: Optional[str]

    salary_range_min: Optional[int]
    salary_range_max: Optional[int]
    salary_currency: Optional[str]
    salary_period: Optional[SalaryPeriod]

    remote_work_policy: Optional[RemoteWorkPolicy]
    inferred_skills: Optional[str]
    last_verified_min: Optional[date]
    last_verified_max: Optional[date]

    is_active: Optional[bool] = False
    size: Optional[conint(ge=1, le=100)] = 10
    pretty: Optional[bool] = False
    scroll_token: Optional[List[Any]] = None

    _parse_scroll_token = validator(
        "scroll_token", pre=True, allow_reuse=True
    )(_parse_scroll_token)
