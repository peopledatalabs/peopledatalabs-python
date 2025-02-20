"""
Client's models for validation.
"""

from enum import Enum
from typing import Optional, Literal

from pydantic.v1 import (
    BaseModel,
    conint,
    root_validator,
)

from ..logger import get_logger


logger = get_logger("models")


class BaseRequestModel(BaseModel):
    """
    Base model for parameters common in all requests.
    """

    pretty: Optional[bool]
    size: Optional[conint(ge=1, le=100)]


class AdditionalParametersModel(BaseModel):
    """
    Model for additional parameters which are shared across different APIs.
    """

    min_likelihood: Optional[conint(ge=1, le=10)]
    required: Optional[str]
    titlecase: Optional[bool]
    data_include: Optional[str]
    include_if_matched: Optional[bool]


class BaseSearchModel(BaseRequestModel):
    """
    Common fields validation model for search APIs (company, person).
    """

    query: Optional[dict]
    sql: Optional[str]
    from_: Optional[conint(ge=0, le=9999)]
    scroll_token: Optional[str]
    titlecase: Optional[bool]

    @root_validator(pre=True)
    def query_or_sql(cls, v):
        """
        Checks only one between 'query' and 'sql' is provided.
        """
        if not bool(v.get("query")) ^ bool(v.get("sql")):
            raise ValueError(
                "It is required to provide a value for either the 'query'"
                " parameter or the 'sql' parameter in order"
                " to receive a successful response."
                " See documentation @"
                " https://docs.peopledatalabs.com/docs/"
                "search-api#building-a-query ,"
                " https://docs.peopledatalabs.com/docs/"
                "company-search-api#building-a-query"
            )

        return v


class FieldEnum(str, Enum):
    """
    Valid values for 'field' parameter of autocomplete API.
    """

    class_ = "class"
    company = "company"
    country = "country"
    industry = "industry"
    location = "location"
    major = "major"
    region = "region"
    role = "role"
    school = "school"
    sub_role = "sub_role"
    skill = "skill"
    title = "title"
    website = "website"


class AutocompleteModel(BaseRequestModel):
    """
    Validator model for autocomplete API.
    """

    field: FieldEnum
    text: Optional[str]
    pretty: Optional[bool]
    titlecase: Optional[bool]


class SkillModel(BaseRequestModel):
    """
    Validator model for skill API.
    """

    skill: str
    pretty: Optional[bool]
    titlecase: Optional[bool]


class JobTitleModel(BaseRequestModel):
    """
    Validator model for job_title API.
    """

    job_title: str
    pretty: Optional[bool]
    titlecase: Optional[bool]


class IPModel(BaseModel):
    """
    Validator model for ip API.
    """

    ip: str
    return_ip_metadata: Optional[bool]
    return_ip_location: Optional[bool]
    return_person: Optional[bool]
    return_if_unmatched: Optional[bool]
    pretty: Optional[bool]
    titlecase: Optional[bool]
    min_confidence: Optional[
        Literal["very high", "high", "moderate", "low", "very low"]
    ]
