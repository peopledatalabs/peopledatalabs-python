<p align="center">
<img src="https://www.peopledatalabs.com/images/logos/company-logo.png" style="background-color: white; padding: 5px 10px;" width="250" alt="People Data Labs Logo">
</p>
<h1 align="center">People Data Labs Python Client</h1>
<p align="center">Official Python client for the People Data Labs API.</p>

<p align="center">
  <a href="https://github.com/peopledatalabs/peopledatalabs-python">
    <img src="https://img.shields.io/badge/repo%20status-Active-limegreen" alt="Repo Status">
  </a>&nbsp;
  <a href="https://pypi.org/project/peopledatalabs/">
    <img src="https://img.shields.io/pypi/v/peopledatalabs.svg?logo=pypi&logoColor=fff&label=PyPI+package&color=limegreen" alt="People Data Labs on PyPI" />
  </a>&nbsp;
  <a href="https://pypi.org/project/peopledatalabs/">
    <img src="https://img.shields.io/pypi/pyversions/peopledatalabs.svg" alt="People Data Labs on PyPI" />
  </a>&nbsp;
  <a href="https://github.com/peopledatalabs/peopledatalabs-python/actions/workflows/python-poetry.yml">
    <img src="https://github.com/peopledatalabs/peopledatalabs-python/actions/workflows/python-poetry.yml/badge.svg" alt="Tests Status" />
  </a>
</p>

## Table of Contents

- [🔧 Installation](#installation)
- [🚀 Usage](#usage)
- [🏝 Sandbox Usage](#sandbox)
- [🌐 Endpoints](#endpoints)
- [📘 Documentation](#documentation)
  - [Upgrading to v2.X.X](#upgrading-to-v2)
  - [Upgrading to v3.X.X](#upgrading-to-v3)
  - [Upgrading to v4.X.X](#upgrading-to-v4)


## 🔧 Installation <a name="installation"></a>

1. Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a package manager for Python.

    ```bash
    pip install peopledatalabs
    ```

2. Sign up for a [free PDL API key](https://www.peopledatalabs.com/signup).

## 🚀 Usage <a name="usage"></a>

First, create the PDLPY client:

```python
from peopledatalabs import PDLPY


# specify your API key
client = PDLPY(
    api_key="YOUR API KEY",
)

```

Then, send requests to any PDL API Endpoint.

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
        f"\nReason: {result.reason};"
        f"\nMessage: {result.json()['error']['message']};"
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
                "name": ["Sean F. Thorne"],
            }
        },
        {
            "metadata": {
                "user_id": "345"
            },
            "params": {
                "profile": ["https://www.linkedin.com/in/haydenconrad/"],
                "first_name": "Hayden",
                "last_name": "Conrad",
            }
        }
    ]
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### By Search (Elasticsearch)

```python
es_query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"location_country": "mexico"}},
                {"term": {"job_title_role": "health"}},
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
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
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
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### By `PDL_ID` (Retrieve API)

```python
result = client.person.retrieve(
    person_id="qEnOZ5Oh0poWnQ1luFBfVw_0000",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### By Fuzzy Enrichment (Identify API)

```python
result = client.person.enrichment(
    name="varun villait",
    pretty=True,
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

### Getting Company Data

#### By Enrichment

```python
result = client.company.enrichment(
    website="peopledatalabs.com",
    pretty=True,
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### By Bulk Enrichment

```python
result = client.company.bulk(
    requests=[
        {
            "metadata": {
                "company_id": "123"
            },
            "params": {
                "profile": "linkedin.com/company/peopledatalabs",
            }
        },
        {
            "metadata": {
                "company_id": "345"
            },
            "params": {
                "profile": "https://www.linkedin.com/company/apple/",
            }
        }
    ]
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
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
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
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
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
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
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Clean Raw Company Strings

```python
result = client.company.cleaner(
    name="peOple DaTa LabS",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Clean Raw Location Strings

```python
result = client.location.cleaner(
    location="455 Market Street, San Francisco, California 94105, US",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Clean Raw School Strings

```python
result = client.school.cleaner(
    name="university of oregon",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Get Job Title Enrichment

```python
result = client.job_title(
    job_title="data scientist",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Get Skill Enrichment

```python
result = client.skill(
    skill="c++",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code}"
        f"\nReason: {result.reason}"
        f"\nMessage: {result.json()['error']['message']}"
    )
```

#### Get IP Enrichment

```python
result = client.ip(
    ip="72.212.42.169",
)
if result.ok:
    print(result.text)
else:
    print(
        f"Status: {result.status_code};"
        f"\nReason: {result.reason};"
        f"\nMessage: {result.json()['error']['message']};"
    )
```

## 🏝 Sandbox Usage <a name="sandbox"></a>
#### To enable sandbox usage, use the sandbox flag on PDLPY

```python
PDLPY(sandbox=True)
```

## 🌐 Endpoints <a name="endpoints"></a>

**Person Endpoints**

| API Endpoint                                                                                    | PDLPY Function                      |
| ----------------------------------------------------------------------------------------------- | ----------------------------------- |
| [Person Enrichment API](https://docs.peopledatalabs.com/docs/enrichment-api)                    | `PDLPY.person.enrichment(**params)` |
| [Person Bulk Enrichment API](https://docs.peopledatalabs.com/docs/bulk-enrichment-api)          | `PDLPY.person.bulk(**params)`       |
| [Person Search API](https://docs.peopledatalabs.com/docs/search-api)                            | `PDLPY.person.search(**params)`     |
| [Person Retrieve API](https://docs.peopledatalabs.com/docs/person-retrieve-api)                 | `PDLPY.person.retrieve(**params)`   |
| [Person Identify API](https://docs.peopledatalabs.com/docs/identify-api)                        | `PDLPY.person.identify(**params)`   |

**Company Endpoints**

| API Endpoint                                                                                    | PDLPY Function                       |
| ----------------------------------------------------------------------------------------------- | ------------------------------------ |
| [Company Enrichment API](https://docs.peopledatalabs.com/docs/company-enrichment-api)           | `PDLPY.company.enrichment(**params)` |
| [Company Bulk Enrichment API](https://docs.peopledatalabs.com/docs/bulk-company-enrichment-api) | `PDLPY.company.bulk(**params)`       |
| [Company Search API](https://docs.peopledatalabs.com/docs/company-search-api)                   | `PDLPY.company.search(**params)`     |

**Supporting Endpoints**

| API Endpoint                                                                              | PDLJS Function                     |
| ----------------------------------------------------------------------------------------- | ---------------------------------- |
| [Autocomplete API](https://docs.peopledatalabs.com/docs/autocomplete-api)                 | `PDLPY.autocomplete(**params)`     |
| [Company Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#companyclean)     | `PDLPY.company.cleaner(**params)`  |
| [Location Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#locationclean)   | `PDLPY.location.cleaner(**params)` |
| [School Cleaner API](https://docs.peopledatalabs.com/docs/cleaner-apis#schoolclean)       | `PDLPY.school.cleaner(**params)`   |
| [Job Title Enrichment API](https://docs.peopledatalabs.com/docs/job-title-enrichment-api) | `PDLPY.job_title(**params)`        |
| [Skill Enrichment API](https://docs.peopledatalabs.com/docs/skill-enrichment-api)         | `PDLPY.skill(**params)`            |
| [IP Enrichment API](https://docs.peopledatalabs.com/docs/ip-enrichment-api)               | `PDLPY.ip(**params)`               |

## 📘 Documentation <a name="documentation"></a>

All of our API endpoints are documented at: https://docs.peopledatalabs.com/

These docs describe the supported input parameters, output responses and also provide additional technical context.

As illustrated in the [Endpoints](#endpoints) section above, each of our API endpoints is mapped to a specific method in the PDLPY class.  For each of these class methods, **all function inputs are mapped as input parameters to the respective API endpoint**, meaning that you can use the API documentation linked above to determine the input parameters for each endpoint.

As an example:

The following is **valid** because `name` is a [supported input parameter to the Person Identify API](https://docs.peopledatalabs.com/docs/identify-api-reference#input-parameters):

```python
PDLPY().person.identify({"name": "varun villait"})
```

Conversely, this would be **invalid** because `fake_parameter` is not an input parameter to the Person Identify API:

```python
PDLPY().person.identify({"fake_parameter": "anything"})
```

### Upgrading to v2.X.X <a name="upgrading-to-v2"></a>

NOTE: When upgrading to v2.X.X from vX.X.X and below, the minimum required python version is now 3.8.

### Upgrading to v3.X.X <a name="upgrading-to-v3"></a>

NOTE: When upgrading to v3.X.X from vX.X.X and below, the minimum required pydantic version is now 2.

### Upgrading to v4.X.X <a name="upgrading-to-v4"></a>

NOTE: When upgrading to v4.X.X from vX.X.X and below, we no longer auto load the API key from the environment variable `PDL_API_KEY`. You must now pass the API key as a parameter to the `PDLPY` class.
