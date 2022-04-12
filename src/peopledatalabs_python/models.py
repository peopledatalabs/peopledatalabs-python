from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
)


class EnrichmentModel(BaseModel):
    name: str = None
    first_name: str = None
    last_name: str = None
    middle_name: str = None
    location: str = None
    street_address: str = None
    locality: str = None
    region: str = None
    countery: str = None
    postal_code: str = None
    company: str = None
    school: str = None
    phone: str = None
    email: EmailStr = None
    email_hash: str = None
    profile: HttpUrl = None
    lid: str = None
    birth_date: str = None
