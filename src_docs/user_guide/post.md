# Creating Objects

When using the WAPI to create objects in the Grid, you will need to build up an object as a Python dictionary of
attributes and values. The object will likely have some attributes which are required. The dictionary is passed into a
POST request as JSON payload.

A POST request to create an object in the Grid will generally take the form:

```python linenums="0"
response = wapi.post('<wapi_object>', json={body}, **kwargs)
```

!!! tip

    The Infoblox NIOS WAPI API is fully documented and available online. You can access the API guide by using 
    the following url path on your Infoblox Grid Manager:

    `https://<grid_mgr>/wapidoc`

    See the WAPI Guide for details on all objects, properties, functions, and parameters.

## Create Network

```python
import sys
from ibx_sdk.nios.gift import Gift

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

# Create the Body
body = {
    "network": "192.168.1.0/24",
    "comment": "this is my test network i'm creating"
}

# Create the Netwokr
response = wapi.post('network', json=body)
```

Our `response` above is an `httpx Response` object, and it will contain a number of properties 
and methods. The ones used most often in working with WAPI data are:

| property/method | Description                                                                          |
|-----------------|--------------------------------------------------------------------------------------|
| `json()`        | A method returns JSON-encoded object of the result (if the result was JSON encoded)  |
| `status_code`   | A property representing the HTTP Status Code (200 is OK, 404 is Not Found and so on) |
| `text`          | A property which returns the content of the response in unicode                      |

We can test the success or failure of the above request by checking for an OK status on the `response` object this is
done like so:

```python linenums="19"
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1)  # Exit program
```

When creating objects, the reference of the object will be returned upon the successful creation

```text linenums="0"
network/ZG5zLm5ldHdvcmskMTkyLjE2OC4zLjAvMjQvMA:192.168.1.0/24/default
```

An unsuccessful call may look like the following:

```text linenums="0"
{
    'Error': 'AdmConDataError: None (IBDataConflictError: IB.Data.Conflict:The network 192.168.1.0/24 already exists.  Select another network.)',
    'code': 'Client.Ibap.Data.Conflict',
    'text': 'The network 192.168.1.0/24 already exists.  Select another network.'
}
```

## Create Host Record

```python
from ibx_sdk.nios.gift import Gift, WapiRequestException

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

# Create the Body
body = {
    "name": "my-router.example.com",
    "ipv4addrs": [
        {
            "ipv4addr": "192.168.0.1"

        }
    ]
}
response = wapi.post('record:host', json=body)
```

We can test the success or failure of the above request by checking for an OK status on the `response` object this is
done like adding the following to our script:

```python linenums="21"
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1)  # Exit program
```

When creating objects, the reference of the object will be returned upon the successful creation

```text linenums="0"
record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5leGFtcGxlLm15LXJvdXRlcg:my-router.example.com/Internal%20DNS
```

An unsuccessful call may look like the following:

```text linenums="0"
{
    'Error': "AdmConDataError: None (IBDataConflictError: IB.Data.Conflict:The record 'my-router example.com' already exists.)", 
    'code': 'Client.Ibap.Data.Conflict', 
    'text': "The record 'my-rou
}
```
