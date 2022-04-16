"""
Client's models for validation.
"""


from typing import Optional

from pydantic import (
    BaseModel,
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
    min_likelihood: Optional[int]
    required: Optional[str]
    titlecase: Optional[bool]
    data_include: Optional[str]
    include_if_matched: Optional[bool]
