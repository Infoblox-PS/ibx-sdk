# Connecting

To establish a connection to your NIOS Grid, you'll need the following bits of information:
- Grid Manager hostname or IP Address
- NIOS Administrative User credentials `username` and `password`
- (optionally) the NIOS version `wapi_ver`

Scripts can be fashioned like the examples provided in this toolkit to obtain these properties
as command line arguments. In addition, you could use a `.env` file or roll your own `config.yaml`
file. The last thing you want to do is hard-code these in your scripts which would be very
insecure. In the Toolkit scripts, we used the Python `@click` module which provides superior
CLI script argument parsing and validation.

There are three (3) ways of instantiating the WAPI class:
1. positional arguments
2. named arguments
3. dictionary of properties or key-value pairs

Assuming we have the above properties and values, we can make a Grid connection as follows:

```python
from ibx_tools.nios.wapi import WAPI

wapi = WAPI()
wapi.grid_mgr = 'infoblox.localdomain'
wapi.wapi_ver = '2.11'
wapi.ssl_verify = False
username = 'admin'
password = 'infoblox'

wapi.connect(username, password)
```
This will attempt to use BASIC AUTH to establish a connection with the Grid Manager
_infoblox.localdomain_ using the _admin_ user account and password. The `wapi.connect()`
method will return an WapiRequestException if the connection fails. This example shows how
to build up the WAPI object one property or attribute at a time. You could alternatively pass
in a dictionary of variables as well. See the following:

```python
from ibx_tools.nios.wapi import WAPI

username = "admin"
password = "infoblox"
props = {
    "grid_mgr": "infoblox.localdomain",
    "wapi_ver": "2.11",
    "verify_ssl": False
}
wapi = WAPI(**props)

wapi.connect(username, password)
```
