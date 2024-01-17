# Introduction

The Infoblox `ibx-sdk` is a library and SDK designed to assist users in developing efficient automation scripts for the
Infoblox NIOS Web API (WAPI). The SDK offers a range of tools for effective API interaction, including the following:

1. The `Gift` wrapper class - The `Gift` class is a wrapper around the Python `requests`, which
   in turn makes it easier to access the Infoblox Web API module.
2. Detailed usage and example documentation
3. Sample operations scripts

!!! note

    **What is `Gift`??**

    `Gift` is an object-oriented Python class which is a wrapper to the Python `requests` package. 
    It specifically builds and extends the `requests.session` module. Why the name "Gift"? We 
    named it `Gift` because of the fact it's a wrapper. Get it?? We'd like to think it will be the 
    "Gift" that keeps on giving... Other names considered were:

    * Cellophane - for its transparent, light-weight wrapping prowess!
    * Bacon - because bacon wrapped anything is good!

    We hope you enjoy!

The `Gift()` Python class is a wrapper for `requests.session`, supporting the same HTTP Request methods that are
supported by the NIOS WAPI. See the table below:

| WAPI Method | Gift Request Method | Description                                                           |
|:-----------:|---------------------|-----------------------------------------------------------------------|
|     GET     | Gift.get()          | An HTTP GET is used to read a single object or fetch multiple objects |
|    POST     | Gift.post()         | The POST method is used to create a new object                        |
|     PUT     | Gift.put()          | The PUT method is used to update an existing object.                  |
|   DELETE    | Gift.delete()       | The DELETE method is used to remove an existing object.               |

!!! note

    There is also a convenience method that has been added to the Gift() class for fetcing a single
    object. The `Gift.getone()` method expects to fetch a single record and returns the record's 
    `_ref`. It raises an exception if it fails to return any data or if it finds > 1 record.

## Installing `ibx-sdk`

```shell
pip install ibx-sdk
```

## Initializing the WAPI class

First, you have to import it into your scripts:

```python
from ibx_sdk.nios.gift import Gift
```

Once imported you can instantiate the class as follows:

```python
from ibx_sdk.nios.gift import Gift

wapi = Gift()
```

!!! tip

    We always recommend installing the Basic API Toolkit into a Python Virtual Environment to avoid polluting your
    global Python module(s) environment.

To create a Python virtual environment, perform this sequence of steps:

```shell
cd ~/workspace

mkdir myproject
cd myproject
python3 -m venv .venv
source .vent/bin/activate
pip install -U pip setuptools
```

The above code was performed on a Mac, it leverages a `workspace` folder that would have all our project(s) and code. We 
create a new project called `myproject` and "install" a virtual environment in that folder with `python3`. We sourced 
the environment on line #6. Last we update the `pip` and `setuptools` modules.

!!! warning

    Always source your Python virutal environment of your project or you may end up polluting your own module space. 

Remember to always source your environment prior to working on your next project:

```shell linenums="0"
source .venv/bin/activate
```

You can deactivate when you are done using/modifying the project code:

```shell linenums="0"
deactivate
```
