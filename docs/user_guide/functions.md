# Calling Functions

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

## Basics 

1. Retrieve the object reference from the network container
2. Fetch 2 available networks from the network container
3. Create the 2 networks received 

To fetch the reference for network container 192.168.0.0/16 from the Grid, we start to create our script with the following:

```python
import sys
from ibx_tools.nios.wapi import WAPI

wapi = WAPI(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

_ref = wapi.getone('networkcontainer',
                    params={'network': '192.168.0.0/16',
                            'network_view': 'default'
                            }
)
```

To fetch the next available 2 networks within the network container 192.168.0.0/16 we add the following to our script:

```python
params = {
    '_function': 'next_available_network'
}

body = {
    'cidr': 24,
    'num': 2,
    'exclude': ['192.168.0.0/24', '192.168.1.0/24']
}
response = wapi.post(_ref, json=body, params=params)
````

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

```python
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1) # Exit program
```

To build/create the two next available networks by the function we called, we add the following to our script:

```python
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
