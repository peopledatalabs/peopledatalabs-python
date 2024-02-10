"""
Models for input parameters of the School APIs.
"""

from typing import Optional

from pydantic.v1 import root_validator

from . import BaseRequestModel


class CleanerModel(BaseRequestModel):
    """
    Validation model for School 'cleaner' API.
    """

    name: Optional[str]
    website: Optional[str]
    profile: Optional[str]

    @root_validator(pre=True)
    def at_least_one(cls, value):
        """
        Checks that at least one parameter is valued.
        """
        if not any(value.values()):
            raise ValueError(
                "At least one between 'name' 'website' or 'profile' is"
                " required. See documentation @"
                " https://docs.peopledatalabs.com/docs/cleaner-apis#parameters"
            )

        return value
