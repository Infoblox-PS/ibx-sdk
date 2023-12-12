# Fetching Objects

Fetching Infoblox objects from the Grid using the NIOS Web RESTful API is without a doubt the most
common task for an administrator. The Basic API Toolkit's WAPI class has been written in such a way
to extend the Python Requests nodule to help programmers do just that! This section of the User
Guide
is devoted to providing a tutorial on how to fetch data from the NIOS Grid. Fetching data from the
Grid is dependent on having a valid connection to the Grid using the `WAPI` Python module.

All WAPI object fetches should take the basic form:

```python
res = wapi.get('<wapi_object>', params={}, **kwargs)
```

!!! tip

    The Infoblox NIOS WAPI API is fully documented and available online. You can access the API guide by using 
    the following url path on your Infoblox Grid Manager:

    `https://<grid_mgr>/wapidoc`

    See the WAPI Guide for details on all objects, properties, functions, and parameters.

The Infoblox NIOS Web RESTful API supports Options when performing GET requests to fetch data. A
couple of these are shown below:

| Method Option                                      | Description                                                                                                                                                                                                                                                                     |
|:---------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `_max_results`                                     | Maximum number of objects to be returned. If set to a negative number the appliance will return an error when the number of returned objects would exceed the setting. The default is -1000. If this is set to a positive number, the results will be truncated when necessary. |
| <div style="white-space: nowrap;">`_return_fields` | List of returned fields separated by commas. The use of _return_fields repeatedly is the same as listing several fields with commas. The default is the basic fields of the object.                                                                                             |

## Basics

To fetch all `network` WAPI objects from the Grid, we'd fashion our script like the following:

```python
from ibx_tools.nios.wapi import WAPI, WapiRequestException

wapi = WAPI(
    grid_mgr='infoblox.localdomain',
    wapi_ver='2.12',
    ssl_verify='/path/to/certfile'
)

wapi.connect(username='admin', password='infoblox')

# fetch all networks
response = wapi.get('network')
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
response = wapi.get('network')
if response.status_code == 200:
    log.info('yay! we succeeded')
else:
    log.error(response.text)
```

Let's assume we got a successful `response` above, to get the JSON-encoded results, all we need to
do is unpack
the results. Simply do the following:

```python
results = response.json()
```

## Query Parameters

This code will fetch all networks (provided we don't hit the max result set limit!). A JSON response
is
returned by this request.

!!! note

    This request is very simple and has no exception handling. If the # of networks in the response 
    exceeded the `_max_results` an Exception is raised. The `_max_results` option defaults to 1000. 
    When performing the above query, we can optionally pass this option w/ a larger value to avoid
    the raised Exception.

The `wapi.get()` method signature supports a `params` option (see the wapi class docs). In order to
set `_max_results` on our previous attempt to fetch all networks, we could adjust this property as
follows:

```python
response = wapi.get('network', params={'_max_results': 10000})
```

The above call now sets the `_max_results` to 10,000 rows of data. 

### Filtering Requests with Query Parameters

You should always try to optimize your API fetches to your desired result set. Here's a few 
written examples:

- fetch all **network** objects which have a Grid DHCP Member named _dhcp01.example.com_ assigned
- fetch all **record:a** objects from the zone _example.com_
- fetch all **record:a** objects from the _example.com_ zone but from the _external_ DNS view

These are filtered lists of objects instead of simply returning:
- fetch all **network** objects
- fetch all **record:a** objects

These would potentially result in exceeding our `_max_results` value of 1000, not to mention it 
would return a lot of other data we'd have to sift through to ultimately ignore. So, it's vital 
to write API requests to be well-thought, filtered, and optimized to your desired result set. 
This is done by using Query Parameters!

To fetch all **network** objects which have a Grid DHCP Member named _dhcp01.example.com_ we 
could perform that query as follows:

```python
response = wapi.get(
    'network',
    params={'member': 'dhcp01.example.com'}
)
```

Behind the scenes, the program would generate an API request that would look something like this:

```
GET https://gm.example.com/wapi/v2.5/network?member=dhcp01.example.com 
```

The NIOS WAPI would return all network object(s) that were configured w/ the Grid DHCP Member 
_dhcp01.example.com_ on them.

To fetch all **record:a** objects from the zone _example.com_, we'd similarly write that as:

```python
response = wapi.get(
    'record:a',
    params={'zone': 'example.com'}
)
```

Query Parameters can be a set of params and you can create compound filters when requesting. To 
fetch all **record:a** from the _example.com_ zone but from the _external_ DNS view, we'd simply 
add to the previous request the `view` parameter as follows:

```python
response = wapi.get(
    'record:a',
    params={'zone': 'example.com', 'view', 'external'}
)
```

!!! tip

    Not all WAPI object properties can be used in searches. You will need to consult the Infoblox
    Web RESTful or WAPI Guide on your local Grid Manager by visiting https://<grid_mgr>/wapidoc for
    more details. 



## Handling Exceptions


