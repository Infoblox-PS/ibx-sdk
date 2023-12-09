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
3. instance variables
4. dictionary of properties or key-value pairs

## Positional Arguments

To establish a connection to a NIOS Grid Manager using positional arguments, use the following:

```python
from ibx_tools.nios.wapi import WAPI

grid_mgr = 'infoblox.localdomain'
wapi_ver = '2.11'
ssl_verify = False
username = 'admin'
password = 'infoblox'

wapi = WAPI(grid_mgr, wapi_ver, ssl_verify)

wapi.connect(username, password)
```

!!! warning

    While this works and is acceptable, we do not recommend using positional arguments. Instead, leverage named
    arguments to remove any abiguity. Positional arguments require specific order - if you get the order wrong
    the method/call will fail and you may have a hard time figuring out how to resolve it.

## Named Arguments

Instead of positional arguments it's recommended you use named args and parameters as shown below:

```python
from ibx_tools.nios.wapi import WAPI

wapi = WAPI(grid_mgr='infoblox.localdomain', wapi_ver='2.11', ssl_verify='/path/to/certfile')
wapi.connect(username='admin', password='infoblox')
```

## Instance Variables

In the next example, we establish our connection to the NIOS Grid Manager by instantiating the `WAPI` class, and
building it up using the `WAPI` class properties.

```python
from ibx_tools.nios.wapi import WAPI

wapi = WAPI()
wapi.grid_mgr = 'infoblox.localdomain'
wapi.wapi_ver = '2.11'
wapi.ssl_verify = '/path/to/certfile'
username = 'admin'
password = 'infoblox'

wapi.connect(username, password)
```

!!! tip

    By instantiating an empty instance of the `WAPI` class, you can make the `wapi` instance variable global instead
    of having to pass it around in your scripts to other functions and methods. See Below.

```python
from ibx_tools.nios.wapi import WAPI

wapi = WAPI()


def get_grid():
    # the wapi instance is visible in the method
    res = wapi.get(f'{wapi.url}/grid')


def main():
    wapi.grid_mgr = 'infoblox.localdomain'
    wapi.wapi_ver = '2.11'
    wapi.ssl_verify = '/path/to/certfile'

    wapi.connect(username='admin', password='infoblox')
    get_grid()
```

line 3 - We're instantiating the `WAPI` class without any attributes set on the instance globally  
lines 12-14 - we build up the `wapi` instance  
line 16 - we establish our connection to the NIOS Grid Manager  
line 17 - we call a method/function in the code to get the Grid object  
lines 6-8 - we make a call with the `wapi` instance. It's visible to the function because we made it global

If a `WAPI` instance is not global, you will need to pass it around to any methods and functions which use it. Our
previous code would now look more like this:

```python
from ibx_tools.nios.wapi import WAPI


def get_grid(wapi):
    # the wapi instance is visible in the method
    res = wapi.get(f'{wapi.url}/grid')


def main():
    wapi = WAPI()
    wapi.grid_mgr = 'infoblox.localdomain'
    wapi.wapi_ver = '2.11'
    wapi.ssl_verify = '/path/to/certfile'

    wapi.connect(username='admin', password='infoblox')
    get_grid(wapi)
```

Notice how we have to pass the `wapi` instance to the `get_grid` function. We MUST do this if the `wapi` instance is a
locally scoped variable instead of a global one.

## Dictionary of properties

In addition to the above, you can instantiate the `WAPI` class using a dictionary and passing that into the
constructor shown below:

```python
from ibx_tools.nios.wapi import WAPI

username = "admin"
password = "infoblox"
props = {
    "grid_mgr": "infoblox.localdomain",
    "wapi_ver": "2.11",
    "verify_ssl": '/path/to/certfile'
}
wapi = WAPI(**props)

wapi.connect(username, password)
```

This will attempt to use BASIC AUTH to establish a connection with the Grid Manager
_infoblox.localdomain_ using the _admin_ user account and password. The `wapi.connect()`
method will return an WapiRequestException if the connection fails. This example shows how
to build up the WAPI object one property or attribute at a time. You could alternatively pass
in a dictionary of variables as well. See the following:
