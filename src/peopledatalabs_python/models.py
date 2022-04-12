"""
Client's models for validation.
"""


from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
)


class EnrichmentModel(BaseModel):
    """
    Model for the enrichment API.
    """
    birth_date: str = None
    company: str = None
    country: str = None
    email: EmailStr = None
    email_hash: str = None
    first_name: str = None
    last_name: str = None
    lid: str = None
    locality: str = None
    location: str = None
    middle_name: str = None
    name: str = None
    phone: str = None
    postal_code: str = None
    profile: HttpUrl = None
    region: str = None
    school: str = None
    street_address: str = None
