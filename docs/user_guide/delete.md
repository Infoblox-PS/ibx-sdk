# Deleting Objects

Creating Infoblox objects from the Grid using the NIOS Web RESTful API is a common task for an 
administrator. The Basic API Toolkit's WAPI class has been written in such a way to extend the 
Python Requests nodule to help programmers do just that! This section of the User Guide is 
devoted to providing a tutorial on how to fetch data from the NIOS Grid. Deleting data from the
Grid is dependent on having a valid connection to the Grid using the `WAPI` Python module.

All WAPI object deletes should take the basic form:   

```python linenums="0"
response = wapi.delete('<wapi_objct_reference>', **kwargs)
```

!!! tip

    The Infoblox NIOS WAPI API is fully documented and available online. You can access the API 
    guide by using the following url path on your Infoblox Grid Manager:

    `https://<grid_mgr>/wapidoc`

    See the WAPI Guide for details on all objects, properties, functions, and parameters.

## Delete Network
1. Retrieve the object reference from the network
2. Delete the network

!!! tip

    The wapi.getone('<wapi_object', params, **kwargs) method does not return a response object. 
    It will return an object reference of type string.

To fetch the reference for network container 192.168.2.0/24 from the Grid, we start to create 
our script with the following:

```python
import sys
from ibx_tools.nios.gift import Gift

wapi = Gift(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
)

wapi.connect(username='admin', password='infoblox')

_ref = wapi.getone('network',
                   params={'network': '192.168.2.0/23',
                           'network_view': 'default'
                           }
)
```

To delete the network we add the following to our script:
```python linenums="0"
response = wapi.delete(_ref)
```

Our `response` above is a Requests response object, and it will contain a number of properties and
methods.

The ones used most often in working with WAPI data are:

| property/method | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| `json()`        | A method returns JSON-encoded object of the result (if the result was JSON encoded) |
| `status_code`   | A property representing the HTTP Status Code (200 is OK, 404 is Not Found and so on) |
| `text`          | A property which returns the content of the response in unicode                     |

We can test the success or failure of the above request by checking for an OK status on the  
`response` object this is done like adding the following to our script:

```python
if response.status_code != 200:
    print(f'We hit a snag {response.text}')
    sys.exit(1) # Exit program
```