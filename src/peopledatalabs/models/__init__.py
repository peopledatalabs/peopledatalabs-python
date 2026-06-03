"""
Client's models for validation.
"""

from enum import Enum
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    Field,
    model_validator,
)

from ..logger import get_logger

logger = get_logger("models")


class BaseRequestModel(BaseModel):
    """
    Base model for parameters common in all requests.
    """

    pretty: bool | None = None
    size: Annotated[int, Field(ge=1, le=100)] | None = None


class AdditionalParametersModel(BaseModel):
    """
    Model for additional parameters which are shared across different APIs.
    """

    min_likelihood: Annotated[int, Field(ge=1, le=10)] | None = None
    required: str | None = None
    titlecase: bool | None = None
    data_include: str | None = None
    include_if_matched: bool | None = None


class BaseSearchModel(BaseRequestModel):
    """
    Common fields validation model for search APIs (company, person).
    """

    query: dict | None = None
    sql: str | None = None
    from_: Annotated[int, Field(ge=0, le=9999)] | None = Field(
        default=None, serialization_alias="from"
    )
    scroll_token: str | None = None
    titlecase: bool | None = None

    @model_validator(mode="before")
    @classmethod
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

    all_location = "all_location"
    class_ = "class"
    company = "company"
    country = "country"
    industry = "industry"
    location = "location"
    location_name = "location_name"
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
    text: str | None = None
    pretty: bool | None = None
    titlecase: bool | None = None


class JobTitleModel(BaseRequestModel):
    """
    Validator model for job_title API.
    """

    job_title: str
    pretty: bool | None = None
    titlecase: bool | None = None


class IPModel(BaseModel):
    """
    Validator model for ip API.
    """

    ip: str
    return_ip_metadata: bool | None = None
    return_ip_location: bool | None = None
    return_person: bool | None = None
    return_if_unmatched: bool | None = None
    pretty: bool | None = None
    titlecase: bool | None = None
    min_confidence: (
        None | (Literal["very high", "high", "moderate", "low", "very low"])
    ) = None
