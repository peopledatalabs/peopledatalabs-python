"""
Models for input parameters of the Person APIs.
"""

from enum import Enum

from typing import Annotated

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

    birth_date: list[str] | str | None = None
    company: list[str] | str | None = None
    country: str | None = None
    email: list[EmailStr] | EmailStr | None = None
    email_hash: list[str] | str | None = None
    first_name: list[str] | str | None = None
    last_name: list[str] | str | None = None
    lid: list[str] | str | None = None
    locality: str | None = None
    location: list[str] | str | None = None
    middle_name: list[str] | str | None = None
    name: list[str] | str | None = None
    phone: list[str] | str | None = None
    pdl_id: list[str] | str | None = None
    postal_code: list[str] | str | None = None
    profile: list[str] | str | None = None
    region: str | None = None
    school: list[str] | str | None = None
    street_address: str | None = None
    pdl_id: str | None = None
    min_likelihood: Annotated[int, Field(ge=1, le=10)] | None = None
    required: str | None = None
    data_include: str | None = None
    include_if_matched: bool | None = None

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

    metadata: dict | None = None
    params: PersonBaseModel = ...


class BulkModel(BaseRequestModel, AdditionalParametersModel):
    """
    Model for the person/bulk API.
    """

    requests: list[PersonBulkParamsModel]

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

    dataset: str | None = None

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

    origin_version: str | None = None
    current_version: str | None = None
    type: str | None = None
    ids: list[str] | None = None
    fields_updated: list[str] | None = None
    scroll_token: str | None = None

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
