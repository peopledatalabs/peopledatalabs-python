"""
Client's models for validation.
"""


from typing import Optional

from pydantic import (
    BaseModel,
    conint
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
    Model for additional parameters which are shared across
    different APIs.
    """
    min_likelihood: Optional[conint(ge=1, le=10)]
    required: Optional[str]
    titlecase: Optional[bool]
    data_include: Optional[str]
    include_if_matched: Optional[bool]
