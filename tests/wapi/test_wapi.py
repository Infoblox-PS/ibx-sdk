"""
WAPI test module
"""
from ibx_tools.nios.wapi import WAPI


def test_instantiate_wapi_without_properties():
    wapi = WAPI()
    assert wapi.grid_mgr is None
    assert wapi.wapi_ver == '2.5'
    assert wapi.ssl_verify is False
    assert isinstance(wapi, WAPI)


def test_instantiate_wapi_with_positional_arguments():
    wapi = WAPI('192.168.1.2', '2.12', '/path/to/certfile')
    assert wapi.grid_mgr == '192.168.1.2'
    assert wapi.wapi_ver == '2.12'
    assert wapi.ssl_verify == '/path/to/certfile'


def test_instantiate_wapi_with_named_arguments():
    wapi = WAPI(grid_mgr='192.168.1.2', wapi_ver='2.12', ssl_verify='/path/to/certfile')
    assert wapi.grid_mgr == '192.168.1.2'
    assert wapi.wapi_ver == '2.12'
    assert wapi.ssl_verify == '/path/to/certfile'


def test_instantiate_wapi_with_dictionary_of_arguments():
    props = dict(grid_mgr='192.168.1.2', wapi_ver='2.12', ssl_verify='/path/to/certfile')
    wapi = WAPI(**props)
    assert wapi.grid_mgr == '192.168.1.2'
    assert wapi.wapi_ver == '2.12'
    assert wapi.ssl_verify == '/path/to/certfile'


def test_ssl_verify_as_string_value():
    wapi = WAPI(ssl_verify='/path/to/certfile')
    assert isinstance(wapi.ssl_verify, str)
    assert wapi.ssl_verify == '/path/to/certfile'


def test_ssl_verify_as_boolean_value():
    wapi = WAPI(ssl_verify=False)
    assert isinstance(wapi.ssl_verify, bool)
    assert wapi.ssl_verify is False


