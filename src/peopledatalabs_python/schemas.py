from pydantic import (
    BaseModel,
    EmailStr,
    HttpUrl,
    SecretStr,
)


class Client(BaseModel):
    api_key: SecretStr
    base_path: HttpUrl = None
    version: str = None


class Person(BaseModel):
    pass


class Enrichment(Person):
    name: str = ""
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    location: str = ""
    street_address: str = ""
    locality: str = ""
    region: str = ""
    countery: str = ""
    postal_code: str = ""
    company: str = ""
    school: str = ""
    phone: str = ""
    email: EmailStr = ""
    email_hash: str = ""
    profile: HttpUrl = ""
    lid: str = ""
    birth_date: str = ""
