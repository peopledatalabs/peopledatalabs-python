"""
Models for input parameters of the Company APIs.
"""

from typing import List, Optional, Union

from pydantic.v1 import (
    BaseModel,
    root_validator,
    validator,
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
    pdl_id: Optional[str]
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
                v.get("pdl_id"),
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


class CompanyBulkParamsModel(BaseModel):
    """
    Model for the validation of the 'params' field in the company bulk API.
    """

    metadata: Optional[dict]
    params: CompanyBaseModel = ...


class CompanyBulkModel(BaseRequestModel, AdditionalParametersModel):
    """
    Model for the company bulk API.
    """

    requests: List[CompanyBulkParamsModel]

    @validator("requests", pre=True)
    def must_contain_params(cls, value):
        """
        Checks that 'requests' is not empty.
        """
        if not value:
            raise ValueError(
                "'requests' cannot be empty."
                " See documentation @"
                # pylint: disable=line-too-long
                # flake8: noqa: E501
                " https://docs.peopledatalabs.com/docs/bulk-company-enrichment-api"
            )

        return value


class SearchModel(BaseSearchModel):
    """
    Search parameters model validator for Company search API.
    """


# pylint: disable=duplicate-code
class CleanerModel(BaseRequestModel):
    """
    Validation model for Company 'cleaner' API.
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
