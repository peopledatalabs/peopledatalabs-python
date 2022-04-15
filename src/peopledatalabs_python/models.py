"""
Client's models for validation.
"""


from typing import List, Union, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    root_validator,
    validator,
)

from .logger import get_logger


logger = get_logger("models")


class BaseRequestModel(BaseModel):
    """
    Base model for parameters common in all requests
    """
    pretty: Optional[bool]


class PersonEnrichmentBaseModel(BaseModel):
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
                " https://docs.peopledatalabs.com/docs/bulk-enrichment-api"
            )
        return value


class PersonEnrichmentOptionalsModel(BaseModel):
    """
    Optional parameters model for the enrichment API.
    """
    min_likelihood: Optional[int]
    required: Optional[str]


class PersonEnrichmentModel(
    BaseRequestModel, PersonEnrichmentBaseModel, PersonEnrichmentOptionalsModel
):
    """
    Model for the enrichment API.
    """


class PersonBulkParamsModel(BaseModel):
    """
    Model for the validation of the 'params' field in the
    person/bulk API.
    """
    metadata: Optional[dict]
    params: PersonEnrichmentBaseModel = ...


class PersonBulkModel(PersonEnrichmentOptionalsModel):
    """
    Model for the person/bulk API
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
