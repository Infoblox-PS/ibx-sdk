# Introduction

The Infoblox Basic API Toolkit is a library and it is a set of tools written to help users create 
effective automation scripts for accessing the Infoblox NIOS Web API or WAPI. The Basic API Toolkit 
provides the following:

1. A WAPI wrapper class - The WAPI class is a wrapper around the Python `requests` module.
2. Detailed usage and example documentation
3. Sample operations scripts

The NIOS WAPI supports the following API methods:

| Method | WAPI Request Method | Description                                                           |
|--------|---------------------|-----------------------------------------------------------------------|
| GET    | WAPI.get()          | An HTTP GET is used to read a single object or fetch multiple objects |
| POST   | WAPI.post()         | The POST method is used to create a new object                        |
| PUT    | WAPI.put()          | The PUT method is used to update an existing object.                  |
| DELETE | WAPI.delete()       | The DELETE method is used to remove an existing object.               |

!!! info

    There is also a convenience method that has been added to the WAPI() class for fetcing a single
    object. The `WAPI.getone()` method expects to fetch a single record and returns the record's 
    `_ref`. It raises an exception if it fails to return any data or if it finds > 1 record.

## Installing the Basic API Toolkit

```shell
pip install ibx-toolkit
```

## Initializing the WAPI class

First, you have to import it into your scripts:

```python
from ibx_tools.nios.gift import Gift
```

Once imported you can instantiate the class as follows:

```python
from ibx_tools.nios.gift import Gift

wapi = Gift()
```
