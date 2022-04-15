"""
Client's models for validation.
"""


from typing import List, Union

from pydantic import (
    BaseModel,
    EmailStr,
)


class BaseRequestModel(BaseModel):
    """
    Base model for parameters common in all requests
    """
    pretty: bool = False


class PersonEnrichmentBaseModel(BaseModel):
    """
    Base parameters model for the enrichment API.
    """
    birth_date: Union[List[str], str] = None
    company: Union[List[str], str] = None
    country: str = None
    email: Union[List[EmailStr], EmailStr] = None
    email_hash: Union[List[str], str] = None
    first_name: Union[List[str], str] = None
    last_name: Union[List[str], str] = None
    lid: Union[List[str], str] = None
    locality: str = None
    location: Union[List[str], str] = None
    middle_name: Union[List[str], str] = None
    name: Union[List[str], str] = None
    phone: Union[List[str], str] = None
    postal_code: Union[List[str], str] = None
    profile: Union[List[str], str] = None
    region: str = None
    school: Union[List[str], str] = None
    street_address: str = None


class PersonEnrichmentOptionalsModel(BaseModel):
    """
    Optional parameters model for the enrichment API.
    """
    min_likelihood: int = None
    required: str = None


class PersonEnrichmentModel(
    BaseRequestModel, PersonEnrichmentBaseModel, PersonEnrichmentOptionalsModel
):
    """
    Model for the enrichment API.
    """
