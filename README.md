<p align="center">
<img src="https://i.imgur.com/S7DkZtr.png" width="250" alt="People Data Labs Logo">
</p>
<h1 align="center">People Data Labs Python Client</h1>
<p align="center">
A Python client for the People Data Labs API.
</p>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/peopledatalabs-python.svg)](https://pypi.python.org/pypi/peopledatalabs-python)
[![PyPI](https://img.shields.io/pypi/pyversions/peopledatalabs-python.svg)](https://pypi.python.org/pypi/peopledatalabs-python)

## Table of Contents
- [🔧 Installation](#installation)
- [🚀 Usage](#usage)
- [🌐 Endpoints](#endpoints)
- [📘 Documentation](#documentation)

## 🔧 Installation <a name="installation"></a>

1. Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a package manager for Python.

    ```bash
    pip install peopledatalabs-python
    ```

2. Sign up for a [free PDL API key](https://www.peopledatalabs.com/signup)

## 🚀 Usage <a name="usage"></a>

First, create the PDLPY client:
```python
from peopledatalabs_python import PDLPY


# specifying an API key
client = PDLPY(
  api_key="YOUR API KEY"
)

# or leave blank if you have API_KEY set in your environment
# (or in a .env file)
client = PDLPY()
```

Then, send requests to any PDL API Endpoint:

### Getting Person Data

#### By Enrichment
```python
result = client.person.enrichment(
    phone="4155688415",
    pretty=True,
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Bulk Enrichment
```python
result = client.person.bulk(
    required="emails AND profiles",
    requests=[
        {
            "metadata": {
                "user_id": "123"
            },
            "params": {
                "profile": ["linkedin.com/in/seanthorne"],
                "location": ["SF Bay Area"],
                "name": ["Sean F. Thorne"]
            }
        },
        {
            "metadata": {
                "user_id": "345"
            },
            "params": {
                "profile": ["https://www.linkedin.com/in/haydenconrad/"],
                "first_name": "Hayden",
                "last_name": "Conrad"
            }
        }
    ]
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Search (Elasticsearch)
```python
es_query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"location_country": "mexico"}},
                {"term": {"job_title_role": "health"}}
            ]
        }
    }
}
data = {
    "query": es_query,
    "size": 10,
    "pretty": True,
    "dataset": "phone, mobile_phone",
}
result = client.person.search(**data)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Search (SQL)
```python
sql_query = (
    "SELECT * FROM person"
    " WHERE location_country='mexico'"
    " AND job_title_role='health'"
    " AND phone_numbers IS NOT NULL;"
)
data = {
    "sql": sql_query,
    "size": 10,
    "pretty": True,
    "dataset": "phone, mobile_phone",
}
result = client.person.search(**data)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By `PDL_ID` (Retrieve API)
```python
result = client.person.retrieve(
    person_id="qEnOZ5Oh0poWnQ1luFBfVw_0000"
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Fuzzy Enrichment (Identify API)
```python
result = client.person.enrichment(
    name="sean thorne",
    pretty=True,
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```

### Getting Company Data
#### By Enrichment
```python
result = client.company.enrichment(
    website="peopledatalabs.com",
    pretty=True
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Search (Elasticsearch)
```python
es_query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"tags": "big data"}},
                {"term": {"industry": "financial services"}},
                {"term": {"location.country": "united states"}},
            ]
        }
    }
}
data = {
    "query": es_query,
    "size": 10,
    "pretty": True,
}
result = client.company.search(**data)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
#### By Search (SQL)
```python
sql_query = (
    "SELECT * FROM company"
    " WHERE tags='big data'"
    " AND industry='financial services'"
    " AND location.country='united states';"
)
data = {
    "sql": sql_query,
    "size": 10,
    "pretty": True,
}
result = client.company.search(**data)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
### Using supporting APIs

#### Get Autocomplete Suggestions
```python
result = client.autocomplete(
    field="title",
    text="full",
    size=10,
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```

#### Clean Raw Company Strings
```python
result = client.company.cleaner(
    name="peOple DaTa LabS"
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```

#### Clean Raw Location Strings
```python
result = client.location.cleaner(
    location="455 Market Street, San Francisco, California 94105, US"
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```

#### Clean Raw School Strings
```python
result = client.school.cleaner(
    name="university of oregon"
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f" Reason: {result.reason};"
        " Message: {};".format(result.json()["error"]["message"])
    )
```
## 🌐 Endpoints <a name="endpoints"></a>

**Person Endpoints**

| API Endpoint | PDLPY Function |
|-|-|
| [Person Enrichment API](https://docs.peopledatalabs.com/docs/enrichment-api) | `PDLPY.person.enrichment(**params)`
| [Person Bulk Enrichment API](https://docs.peopledatalabs.com/docs/bulk-enrichment-api) | `PDLPY.person.bulk(**params)`
| [Person Search API](https://docs.peopledatalabs.com/docs/search-api) | `PDLPY.person.search(**params)`
| [Person Retrieve API](https://docs.peopledatalabs.com/docs/person-retrieve-api) | `PDLPY.person.retrieve(**params)`
| [Person Identify API](https://docs.peopledatalabs.com/docs/identify-api) | `PDLPY.person.identify(**params)` |

**Company Endpoints**

| API Endpoint | PDLPY Function |
|-|-|
| [Company Enrichment API](https://docs.peopledatalabs.com/docs/company-enrichment-api) | `PDLPY.company.enrichment(**params)` |
| [Company Search API](https://docs.peopledatalabs.com/docs/company-search-api) | `PDLPY.company.search(**params)` |

**Supporting Endpoints**

| API Endpoint | PDLJS Function |
|-|-|
| [Autocomplete API](https://docs.peopledatalabs.com/docs/autocomplete-api) | `PDLPY.autocomplete(**params)` |
| [Company Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#companyclean) | `PDLPY.company.cleaner(**params)` |
| [Location Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#locationclean) | `PDLPY.location.cleaner(**params)` |
| [School Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#schoolclean) | `PDLPY.school.cleaner(**params)` |


## 📘 Documentation <a name="documentation"></a>

All of our API endpoints are documented at: https://docs.peopledatalabs.com/

These docs describe the supported input parameters, output responses and also provide additional technical context.

As illustrated in the [Endpoints](#endpoints) section above, each of our API endpoints is mapped to a specific method in the PDLPY class.  For each of these class methods, **all function inputs are mapped as input parameters to the respective API endpoint**, meaning that you can use the API documentation linked above to determine the input parameters for each endpoint.

As an example:

The following is **valid** because `name` is a [supported input parameter to the Person Identify API](https://docs.peopledatalabs.com/docs/identify-api-reference#input-parameters):
```python
PDLPY().person.identify({ name: 'sean thorne' })
```

Conversely, this would be **invalid** because `fake_parameter` is not an input parameter to the Person Identify API:
```python
PDLPY().person.identify({ fake_parameter: 'anything' })
```
