<p align="center">
<img src="https://i.imgur.com/S7DkZtr.png" width="250" alt="People Data Labs Logo">
</p>
<h1 align="center">People Data Labs Python Client</h1>
<p align="center">
A Python client for the People Data Labs API.
</p>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of Contents
- [🔧 Installation](#installation)
- [🚀 Usage](#usage)
- [🌐 Endpoints](#endpoints)
- [📘 Documentation](#documentation)

## 🔧 Installation <a name="installation"></a>

1. Clone this git repo:
```bash
git clone https://github.com/peopledatalabs/peopledatalabs-python.git
```

2. From the root of the repo, run:
```bash
pip install -e .
```

3. Sign up for a [free PDL API key](https://www.peopledatalabs.com/signup)

## 🚀 Usage <a name="usage"></a>

First, create the PDLPY client:
```python
from pepoledatalabs_python import PDLPY


# specifying an API key
client = PDLPY(
  api_key="YOUR API KEY"
)

# or leave blank if you have API_KEY set in your environment
# (or in a .env file)
client = PDLPY()
```

Then, send requests to any PDL API Endpoint:

**Getting Person Data**
```python
# By Enrichment
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

# By Bulk Enrichment
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

# By Search (Elasticsearch)
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

# By PDL_ID (Retrieve API)
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

# By Fuzzy Enrichment (Identify API)
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

**Getting Company Data**
```python
# By Enrichment
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
## 🌐 Endpoints <a name="endpoints"></a>

**Person Endpoints**

| API Endpoint | PDLPY Function |
|-|-|
| [Person Enrichment API](https://docs.peopledatalabs.com/docs/enrichment-api) | `PDLPY.person.enrichment(**params)`
| [Person Bulk Enrichment API](https://docs.peopledatalabs.com/docs/bulk-enrichment-api) | `PDLPY.person.bulk(**params)`
| [Person Search API](https://docs.peopledatalabs.com/docs/search-api) | `PDLPY.person.search(**params)`
| [Person Retrieve API](https://docs.peopledatalabs.com/docs/person-retrieve-api) | `PDLPY.person.retrieve(**params)`
| [Person Identify API](https://docs.peopledatalabs.com/docs/identify-api) | `PDLPY.person.identify(**params)`

**Company Endpoints**
| API Endpoint | PDLPY Function |
|-|-|
| [Company Enrichment API](https://docs.peopledatalabs.com/docs/company-enrichment-api) | `PDLPY.company.enrichment(**params)` |

## 📘 Documentation <a name="documentation"></a>

All of our API endpoints are documented at: https://docs.peopledatalabs.com/

These docs describe the supported input parameters, output responses and also provide additional technical context.
