"""
Client's models for validation.
"""


from typing import Optional

from pydantic import (
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
    size: Optional[conint(ge=1, le=100)]
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


class BaseCleanerModel(BaseRequestModel):
    """
    Common fields validation model for 'cleaner' APIs.
    """

    name: Optional[str]
    website: Optional[str]
    profile: Optional[str]
