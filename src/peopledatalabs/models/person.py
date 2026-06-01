"""
Models for input parameters of the Person APIs.
"""

from enum import Enum
from typing import Annotated, List, Optional, Union

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from . import (
    AdditionalParametersModel,
    BaseRequestModel,
    BaseSearchModel,
)


class PersonBaseModel(BaseModel):
    """
    Base parameters model for the enrichment and identify API.
    """

    birth_date: Optional[Union[List[str], str]] = None
    company: Optional[Union[List[str], str]] = None
    country: Optional[str] = None
    email: Optional[Union[List[EmailStr], EmailStr]] = None
    email_hash: Optional[Union[List[str], str]] = None
    first_name: Optional[Union[List[str], str]] = None
    last_name: Optional[Union[List[str], str]] = None
    lid: Optional[Union[List[str], str]] = None
    locality: Optional[str] = None
    location: Optional[Union[List[str], str]] = None
    middle_name: Optional[Union[List[str], str]] = None
    name: Optional[Union[List[str], str]] = None
    phone: Optional[Union[List[str], str]] = None
    pdl_id: Optional[Union[List[str], str]] = None
    postal_code: Optional[Union[List[str], str]] = None
    profile: Optional[Union[List[str], str]] = None
    region: Optional[str] = None
    school: Optional[Union[List[str], str]] = None
    street_address: Optional[str] = None
    pdl_id: Optional[str] = None
    min_likelihood: Optional[Annotated[int, Field(ge=1, le=10)]] = None
    required: Optional[str] = None
    data_include: Optional[str] = None
    include_if_matched: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
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


class EnrichmentModel(
    BaseRequestModel, PersonBaseModel, AdditionalParametersModel
):
    """
    Model for the enrichment API.
    """


class IdentifyModel(
    BaseRequestModel, PersonBaseModel, AdditionalParametersModel
):
    """
    Model for the identify API.

    The identify API uses same fields for parameters as the enrichment
    API, with the only difference that none of the fields accept
    multiple values.
    """

    @model_validator(mode="before")
    @classmethod
    def no_lists(cls, v):
        """
        Checks none of the values are lists.
        """
        are_lists = [isinstance(field, list) for field in v.values()]
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
    Model for the validation of the 'params' field in the person/bulk API.
    """

    metadata: Optional[dict] = None
    params: PersonBaseModel = ...


class BulkModel(BaseRequestModel, AdditionalParametersModel):
    """
    Model for the person/bulk API.
    """

    requests: List[PersonBulkParamsModel]

    @field_validator("requests", mode="before")
    @classmethod
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


class SearchModel(BaseSearchModel):
    """
    Model for validation of person search API.
    """

    dataset: Optional[str] = None

    @field_validator("dataset", mode="before")
    @classmethod
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


class ChangelogModel(BaseModel):
    """
    Model for validation of person changelog API.
    """

    origin_version: Optional[str] = None
    current_version: Optional[str] = None
    type: Optional[str] = None
    ids: Optional[List[str]] = None
    fields_updated: Optional[List[str]] = None
    scroll_token: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def check_required_fields(cls, values):
        """
        Validate that:
        - origin_version and current_version are both provided.
        - Either 'ids' or 'type' is provided.
        """
        origin = values.get("origin_version")
        current = values.get("current_version")
        ids = values.get("ids")
        typ = values.get("type")

        if not origin:
            raise ValueError("origin_version must be provided.")
        if not current:
            raise ValueError("current_version must be provided.")
        if not ids and not typ:
            raise ValueError("Either 'ids' or 'type' must be provided.")

        return values
