# Calling Functions

Numerous WAPI objects support the ability to call functions on objects. Functions are generally called by issuing a
POST request, along with a set of attributes and associated values in a Python Dictionary. The dictionary of
properties are sent as a JSON body in the request. Object function calls to WAPI object generally take the form:

```python linenums="0"
response = wapi.post('<wapi_object>', json={body}, **kwargs)
```

!!! tip

    The Infoblox NIOS WAPI API is fully documented and available online. You can access the API guide by using 
    the following url path on your Infoblox Grid Manager:

    `https://<grid_mgr>/wapidoc`

    See the WAPI Guide for details on all objects, properties, functions, and parameters.

## Next Available Network

1. Retrieve the object reference from the network container
2. Fetch 2 available networks from the network container
3. Create the 2 networks received

!!! tip

    The `wapi.getone('<wapi_object>', params, **kwargs)` method does not return a response object. 
    It will return an object reference of type string.

To fetch the reference for network container 192.168.0.0/16 from the Grid, we start to create our script with the
following:

```python
import sys
from ibx_sdk.nios.gift import Gift

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

_ref = wapi.getone(
    'networkcontainer',
    params={
        'network': '192.168.0.0/16',
        'network_view': 'default'
    }
)
```

To fetch the next available 2 networks within the network container 192.168.0.0/16 we add the following to our script:

```python  linenums="18"
params = {
    '_function': 'next_available_network'
}

body = {
    'cidr': 24,
    'num': 2,
    'exclude': ['192.168.0.0/24', '192.168.1.0/24']
}
response = wapi.post(_ref, json=body, params=params)
```

Our `response` above is a Requests response object, and it will contain a number of properties and
methods.

The ones used most often in working with WAPI data are:

| property/method | Description                                                                          |
|-----------------|--------------------------------------------------------------------------------------|
| `json()`        | A method returns JSON-encoded object of the result (if the result was JSON encoded)  |
| `status_code`   | A property representing the HTTP Status Code (200 is OK, 404 is Not Found and so on) |
| `text`          | A property which returns the content of the response in unicode                      |

We can test the success or failure of the above request by checking for an OK status on the `response` object this
is done like adding the following to our script:

```python linenums="28"
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1)  # Exit program
```

To build/create the two next available networks by the function we called, we add the following to our script:

```python linenums="31"
networks_dict = response.json()

for network in networks_dict['networks']:
    body = {
        "network": network,
        "comment": "created from next available network routine"
    }

    response = wapi.post('network', json=body)
    if response.status_code == 201:
        print(f'Yay!!!! Network Created {response.json()}')
    else:
        print(f'error: {response.text}')
```

## Next Available IP

1. Retrieve the object reference from the network
2. Fetch 10 available networks from the network
3. Create the 10 IP Reservations from the ips received

To fetch the reference for network container 192.168.2.0/24 from the Grid, we start to create our script with the
following:

```python
import sys
from ibx_sdk.nios.gift import Gift

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

my_network = '192.168.2.0/24'

# Retrieve the reference for my_network
_ref = wapi.getone(
    'network',
    params={
        'network': my_network,
        'network_view': 'default'
    }
)
```

To fetch the next 10 available ips within the network 192.168.2.0/24 we add the following to our script:

```python  linenums="21"
params = {
    '_function': 'next_available_ip'
}

# Create the Body of the request
body = {
    'num': 10,
    'exclude': ['192.168.2.1', '192.168.2.2']
}
response = wapi.post(_ref, json=body, params=params)

if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1)  # Exit program
```

To build/create the 10 fixed addresses recevied by the function we called, we add the following to our script:

```python linenums="35"
for ip in ip_dict['ips']:
    body = {
        "network": my_network,
        "ipv4addr": ip,
        'match_client': 'RESERVED',
        "comment": "created from next available ip routine"
    }

    response = wapi.post('fixedaddress', json=body)
    if response.status_code == 201:
        print(f'Yay!!!! Reservation Created {response.json()}')
    else:
        print(f'error: {response.text}')
```

## Expand Network

1. Retrieve the object reference from the network
2. Expand Network to a /23

To fetch the reference for network container 192.168.2.0/24 from the Grid, we start to create our script with the
following:

```python
import sys
from ibx_sdk.nios.gift import Gift

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

my_network = '192.168.2.0/24'

# Retrieve the reference for my_network
_ref = wapi.getone(
    'network',
    params={
        'network': my_network,
        'network_view': 'default'
    }
)
```

Expand network to 192.168.2.0/23 we add the following to our script:

```python linenums="21"
params = {
    '_function': 'expand_network'
}

# Create the Body of the request
body = {
    'prefix': 23,
}

# Get the Network(s)
response = wapi.post(_ref, json=body, params=params)
```

!!! Danger

    This function reduces the subnet masks of a network by joining all networks that fall under it. All the ranges and
    fixed addresses of the original networks are reparented to the new joined network. Any network containers that fall
    inside the bounds of the joined network are removed. The member assignments for all the encompassed networks are
    joined together. The default router, broadcast address, and subnet mask overrided from the joined network,
    including the ranges and fixed addresses, are all cleaned up.
