# Introduction

The Infoblox Basic API Toolkit is a library and it is a set of tools written to help users create 
effective automation scripts for accessing the Infoblox NIOS Web API or WAPI. The Basic API Toolkit 
provides the following:

1. The `Gift` wrapper class - The `Gift` class is a wrapper around the Python `requests`, which 
   in turn makes it easier to access the Infoblox Web API module.
2. Detailed usage and example documentation
3. Sample operations scripts

The `Gift` Python `requests.session` wrapper supports the same HTTP Request methods that are 
supported by the NIOS WAPI. See the table below:

| WAPI Method | Gift Request Method | Description                                                           |
|:-----------:|---------------------|-----------------------------------------------------------------------|
|     GET     | Gift.get()          | An HTTP GET is used to read a single object or fetch multiple objects |
|    POST     | Gift.post()         | The POST method is used to create a new object                        |
|     PUT     | Gift.put()          | The PUT method is used to update an existing object.                  |
|   DELETE    | Gift.delete()       | The DELETE method is used to remove an existing object.               |

!!! info

    There is also a convenience method that has been added to the Gift() class for fetcing a single
    object. The `Gift.getone()` method expects to fetch a single record and returns the record's 
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

!!! tip

    We always recommend installing the Basic API Toolkit into a Python Virtual Environment to 
    avoid polluting your global Python module(s) environment.
