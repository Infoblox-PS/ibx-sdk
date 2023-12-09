# Introduction / Overview

The Infoblox Basic API Toolkit is a set of tools written to help users create effective automation scripts 
for accessing the Infoblox NIOS Web API or WAPI. The Basic API Toolkit provides the following:

1. A WAPI wrapper class - The WAPI class is a wrapper around the Python `requests` module.
2. Detailed usage and example documentation
3. A set of example scripts 

## Installing the Basic API Toolkit

```shell
pip install ibx-toolkit
```
## Initializing the WAPI class

First, you have to import it into your scripts:

```python
from ibx_tools.nios.wapi import WAPI
```

Once imported you can instantiate the class as follows:

```python
from ibx_tools.nios.wapi import WAPI

wapi = WAPI()
```
