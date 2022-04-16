"""
Client's models for validation.
"""


from enum import Enum
from typing import List, Union, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    conint,
    root_validator,
    validator,
)

from .logger import get_logger


logger = get_logger("models")


class BaseRequestModel(BaseModel):
    """
    Base model for parameters common in all requests.
    """
    pretty: Optional[bool]


class PersonBaseModel(BaseModel):
    """
    Base parameters model for the enrichment API.
    """
    birth_date: Optional[Union[List[str], str]]
    company: Optional[Union[List[str], str]]
    country: Optional[str]
    email: Optional[Union[List[EmailStr], EmailStr]]
    email_hash: Optional[Union[List[str], str]]
    first_name: Optional[Union[List[str], str]]
    last_name: Optional[Union[List[str], str]]
    lid: Optional[Union[List[str], str]]
    locality: Optional[str]
    location: Optional[Union[List[str], str]]
    middle_name: Optional[Union[List[str], str]]
    name: Optional[Union[List[str], str]]
    phone: Optional[Union[List[str], str]]
    postal_code: Optional[Union[List[str], str]]
    profile: Optional[Union[List[str], str]]
    region: Optional[str]
    school: Optional[Union[List[str], str]]
    street_address: Optional[str]

    @root_validator(pre=True)
    def at_least_one(cls, value):
        """
        Checks that at least one parameter is valued.
        """
        if not any(value.values()):
            raise ValueError(
                "'params' cannot be empty."
                " See documentation @"
                " https://docs.peopledatalabs.com/docs/enrichment-api"
            )

        return value


class PersonOptionalsModel(BaseModel):
    """
    Optional parameters model for the enrichment API.
    """
    min_likelihood: Optional[int]
    required: Optional[str]
    titlecase: Optional[bool]
    data_include: Optional[str]
    include_if_matched: Optional[bool]


class PersonEnrichmentModel(
    BaseRequestModel, PersonBaseModel, PersonOptionalsModel
):
    """
    Model for the enrichment API.
    """


class PersonIdentifyModel(
    BaseRequestModel, PersonBaseModel, PersonOptionalsModel
):
    """
    Model for the identify API.

    The identify API uses same fields for parameters as the enrichment
    API, with the only difference that none of the fields accept
    multiple values.
    """

    @root_validator(pre=True)
    def no_lists(cls, v):
        """
        Checks none of the values are lists.
        """
        are_lists = [
            isinstance(field, list) for field in v.values()
        ]
        if any(are_lists):
            raise ValueError(
                "Identify API does not take multiple values"
                " for parameters. See documentation @ "
                "https://docs.peopledatalabs.com/docs/"
                "identify-api-input-parameters"
            )

        return v


class PersonBulkParamsModel(BaseModel):
    """
    Model for the validation of the 'params' field in the
    person/bulk API.
    """
    metadata: Optional[dict]
    params: PersonBaseModel = ...


class PersonBulkModel(BaseRequestModel, PersonOptionalsModel):
    """
    Model for the person/bulk API.
    """
    requests: List[PersonBulkParamsModel]

    @validator("requests", pre=True)
    def must_contain_params(cls, value):
        """
        Checks that 'requests' is not empty.
        """
        if not value:
            raise ValueError(
                "'requests' cannot be empty."
                " See documentation @"
                " https://docs.peopledatalabs.com/docs/bulk-enrichment-api"
            )

        return value


class DatasetEnum(str, Enum):
    """
    Valid values for 'dataset' field of search API.
    """
    resume = "resume"
    email = "email"
    phone = "phone"
    mobile_phone = "mobile_phone"
    street_address = "street_address"
    consumer_social = "consumer_social"
    developer = "developer"
    all = "all"


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


class PersonSearchModel(BaseSearchModel):
    """
    Model for validation of person search API.
    """
    dataset: Optional[str]

    @validator("dataset", pre=True)
    def validate_datasets(cls, v):
        """
        Checks each passed dataset to be of the allowed ones.
        """
        res = []
        for dataset in [e.strip() for e in v.split(",") if e]:
            if dataset.startswith("-"):
                res.append("-" + DatasetEnum(dataset[1:]))
            else:
                res.append(DatasetEnum(dataset))

        return ",".join(res)
