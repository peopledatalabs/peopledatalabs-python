"""
Models for input parameters of the Location APIs.
"""

from . import BaseRequestModel


class CleanerModel(BaseRequestModel):
    """
    Validation model for Location 'cleaner' API.
    """

    location: str
