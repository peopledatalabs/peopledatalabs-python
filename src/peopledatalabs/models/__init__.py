"""
Client's models for validation.
"""

from enum import Enum
from typing import Annotated, Optional, Literal

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

    pretty: Optional[bool] = None
    size: Optional[Annotated[int, Field(ge=1, le=100)]] = None


class AdditionalParametersModel(BaseModel):
    """
    Model for additional parameters which are shared across different APIs.
    """

    min_likelihood: Optional[Annotated[int, Field(ge=1, le=10)]] = None
    required: Optional[str] = None
    titlecase: Optional[bool] = None
    data_include: Optional[str] = None
    include_if_matched: Optional[bool] = None


class BaseSearchModel(BaseRequestModel):
    """
    Common fields validation model for search APIs (company, person).
    """

    query: Optional[dict] = None
    sql: Optional[str] = None
    from_: Optional[Annotated[int, Field(ge=0, le=9999)]] = Field(
        default=None, serialization_alias="from"
    )
    scroll_token: Optional[str] = None
    titlecase: Optional[bool] = None

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
    text: Optional[str] = None
    pretty: Optional[bool] = None
    titlecase: Optional[bool] = None


class JobTitleModel(BaseRequestModel):
    """
    Validator model for job_title API.
    """

    job_title: str
    pretty: Optional[bool] = None
    titlecase: Optional[bool] = None


class IPModel(BaseModel):
    """
    Validator model for ip API.
    """

    ip: str
    return_ip_metadata: Optional[bool] = None
    return_ip_location: Optional[bool] = None
    return_person: Optional[bool] = None
    return_if_unmatched: Optional[bool] = None
    pretty: Optional[bool] = None
    titlecase: Optional[bool] = None
    min_confidence: Optional[
        Literal["very high", "high", "moderate", "low", "very low"]
    ] = None
