"""
Models for input parameters of the School APIs.
"""

from pydantic import model_validator

from . import BaseRequestModel


class CleanerModel(BaseRequestModel):
    """
    Validation model for School 'cleaner' API.
    """

    name: str | None = None
    website: str | None = None
    profile: str | None = None

    @model_validator(mode="before")
    @classmethod
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
