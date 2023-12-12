# Creating Objects

Creating Infoblox objects from the Grid using the NIOS Web RESTful API is a 
common task for an administrator. The Basic API Toolkit's WAPI class has been written in such a way
to extend the Python Requests nodule to help programmers do just that! This section of the User
Guide is devoted to providing a tutorial on how to fetch data from the NIOS Grid. Posting data from the
Grid is dependent on having a valid connection to the Grid using the `WAPI` Python module.

All WAPI object posts should take the basic form:

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
from ibx_tools.nios.gift import Gift

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

Our `response` above is a Requests response object, and it will contain a number of properties and
methods.
The ones used most often in working with WAPI data are:

| property/method | Description                                                                          |
|-----------------|--------------------------------------------------------------------------------------|
| `json()`        | A method returns JSON-encoded object of the result (if the result was JSON encoded)  |
| `status_code`   | A property representing the HTTP Status Code (200 is OK, 404 is Not Found and so on) |
| `text`          | A property which returns the content of the response in unicode                      |

We can test the success or failure of the above request by checking for an OK status on
the `response` object this is done like so:

```python
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1) # Exit program
```

When creating objects, the reference of the object will be retured upon the successful creation
```text linenums="0"
network/ZG5zLm5ldHdvcmskMTkyLjE2OC4zLjAvMjQvMA:192.168.1.0/24/default
```

An unsessful call may look like the following:
```text linenums="0"
{
    'Error': 'AdmConDataError: None (IBDataConflictError: IB.Data.Conflict:The network 192.168.1.0/24 already exists.  Select another network.)',
    'code': 'Client.Ibap.Data.Conflict',
    'text': 'The network 192.168.1.0/24 already exists.  Select another network.'
}
```

## Create Host Record

```python
from ibx_tools.nios.gift import Gift, WapiRequestException

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

We can test the success or failure of the above request by checking for an OK status on the 
`response` object this is done like adding the following to our script:

```python
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1) # Exit program
```

When creating objects, the reference of the object will be retured upon the successful creation
```text linenums="0"
record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5leGFtcGxlLm15LXJvdXRlcg:my-router.example.com/Internal%20DNS
```

An unsessful call may look like the following:
```text linenums="0"
{
    'Error': "AdmConDataError: None (IBDataConflictError: IB.Data.Conflict:The record 'my-router example.com' already exists.)", 
    'code': 'Client.Ibap.Data.Conflict', 
    'text': "The record 'my-rou
}
```
