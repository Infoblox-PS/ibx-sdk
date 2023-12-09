"""
WAPI test module
"""
import urllib3

from ibx_tools.nios.wapi import WAPI, WapiRequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


def test_wapi_basic_auth_connection():
    wapi = WAPI(grid_mgr='192.168.40.60', wapi_ver='2.12', ssl_verify=False)
    wapi.connect(username='admin', password='infoblox')
    assert wapi.grid_ref is not None


def test_wapi_basic_auth_connection_with_bad_password():
    wapi = WAPI(grid_mgr='192.168.40.60', wapi_ver='2.12', ssl_verify=False)
    try:
        wapi.connect(username='admin', password='bad_password')
    except WapiRequestException as err:
        assert '401 Client Error: Authorization Required' in str(err)
    assert wapi.grid_ref is None
