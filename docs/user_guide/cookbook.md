# Cookbook / Recipes

## Using search modifiers with Query Params

The Infoblox NIOS WAPI supports the following Search Modifiers:

| Modifier | Functionality                                         |
|:--------:|-------------------------------------------------------|
|    !     | Negates the condition, or not _x_                     |
|    :     | Makes string matching case insensitive                |
|    ~     | Regular expression search. Expressions are unanchored |
|    <     | Less than or equal                                    |
|    >     | Greater than or equal                                 | 

!!! note

    Integers and dates support: !, < and >
    All other types behave like strings and support: !, ~, and :

```python
response = wapi.get(
    'network',
    params={'*Building:': 'Data Center'}
)
```

This query is an example of a case-insensitive search for all networks which contain the 
Extensible Attribute or EA of **Building** with a value of **data center**. Searches for 
extensible attributes are sent by prefixing the extensible attribute name with an asterisk (*).

## Regex searches in Query Params

Some object properties allow you to search using regular expressions. The **network** object for 
example, allows you to search using regular expression on the `network` property. The following 
is an example of a regular expression search for all networks in the 172.16.0.0/16 space:

```python
response = wapi.get(
    'network',
    params={'network~': '^172\.16\.'}
)
```

## Updating EAs on objects

```python
ea_data = {
    'extattrs-': {
        'attrstring': {},
        'attrinteger': {}
    }
}
wapi.put(network_ref, json=ea_data)
```

```python
ea_data = {
    'extattrs-': {
        'attrstring': {'value': 'test string'},
    }
}
wapi.put(network_ref, json=ea_data)
```

```python
ea_data = {
    'extattrs+': {
        'attrstring': {'value': 'new string'},
    }
}
wapi.put(network_ref, json=ea_data)
```

```python
ea_data = {
    "extattrs": {
        "attrstring": {"value": "test string"},
        "attrinteger": {"value": -1},
        "attremail": {"value": "test@test.com"},
        "attrdate": {"value": "2011-11-23T11:01:00Z"},
        "attrenum": {"value": "Enum Value"},
    }
}
wapi.put(network_ref, json=ea_data)
```

## Using the `request` Object

The `request` object allows the control of WAPI calls through a single entry point. The object 
supports only the POST method and does not support URI arguments. 

The following code uses the `request` object to issue two (2) DNS dig requests to different Grid 
Members:

```python
body = [{
  "method":"POST",
  "object":"grid",
  "args":{"_function":"query_fqdn_on_member"},
  "data":{
    "name_server":"8.8.8.8",
    "fqdn":"infoblox.com",
    "record_type":"A",
    "member":"gm.blox.corp"
  }
},
{
  "method":"POST",
  "object":"grid",
  "args":{"_function":"query_fqdn_on_member"},
  "data":{
    "name_server":"8.8.8.8",
    "fqdn":"infoblox.com",
    "record_type":"A",
    "member":"gmc.blox.corp"
  }
}]
response = wapi.post(
    'request',
    json=body
)
```
