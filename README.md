<p align="center">
<img src="https://i.imgur.com/S7DkZtr.png" width="250" alt="People Data Labs Logo">
</p>
<h1 align="center">People Data Labs Python Client</h1>
<p align="center">
A Python client for the People Data Labs API.
</p>

## Table of Contents
- [🚀 Usage](#usage)
- [🌐 Endpoints](#endpoints)
- [📘 Documentation](#documentation)

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
    phone="4155688415"
)
if result["status"] == 200:
    print(result["data"])
else:
    print(
        "Status: {status};"
        " Error: {type};"
        " Message: {message}".format(**result, **result["error"])
    )
```
## 🌐 Endpoints <a name="endpoints"></a>

**Person Endpoints**

| API Endpoint | PDLPY Function |
|-|-|
| [Person Enrichment API](https://docs.peopledatalabs.com/docs/enrichment-api) | `PDLPY.person.enrichment(...params)`

## 📘 Documentation <a name="documentation"></a>

All of our API endpoints are documented at: https://docs.peopledatalabs.com/

These docs describe the supported input parameters, output responses and also provide additional technical context.
