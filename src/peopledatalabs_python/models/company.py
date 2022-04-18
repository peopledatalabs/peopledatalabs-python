"""
Models for input parameters of the Person APIs.
"""


from typing import List, Optional, Union

from pydantic import (
    BaseModel,
    root_validator,
)

from . import (
    AdditionalParametersModel,
    BaseRequestModel,
    BaseSearchModel,
)


class CompanyBaseModel(BaseModel):
    """
    Base parameters model for the enrichment API.
    """

    country: Optional[str]
    locality: Optional[str]
    location: Optional[Union[List[str], str]]
    name: Optional[str]
    postal_code: Optional[str]
    profile: Optional[str]
    region: Optional[str]
    street_address: Optional[str]
    ticker: Optional[str]
    website: Optional[str]

    @root_validator(pre=True)
    def non_ambiguous(cls, v):
        """
        Checks that at leat one between 'name', 'ticker', 'website' and
        'profile' is given.
        """
        if not any(
            [
                v.get("name"),
                v.get("profile"),
                v.get("ticker"),
                v.get("website"),
            ]
        ):
            raise ValueError(
                "Company Enrichment API requires a non-ambiguous match."
                " See documentation @"
                " https://docs.peopledatalabs.com/docs/enrichment-api"
            )

        return v


class EnrichmentModel(
    BaseRequestModel, CompanyBaseModel, AdditionalParametersModel
):
    """
    Model for the enrichment API.
    """


class SearchModel(BaseSearchModel):
    """
    Search parameters model validator for Company search API.
    """
