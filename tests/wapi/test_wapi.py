"""
WAPI test module
"""
import os

import urllib3

from ibx_tools.nios.wapi import WAPI, WapiRequestException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get('GRID_MGR')
WAPI_VER = os.environ.get('WAPI_VER')
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')
SSL_VERIFY = False if os.environ.get('SSL_VERIFY') == 'False' else True


def test_instantiate_wapi_without_properties():
    wapi = WAPI()
    assert wapi.grid_mgr is None
    assert wapi.wapi_ver == '2.5'
    assert wapi.ssl_verify is False
    assert isinstance(wapi, WAPI)


def test_instantiate_wapi_with_positional_arguments():
    wapi = WAPI(GRID_MGR, WAPI_VER, SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_instantiate_wapi_with_named_arguments():
    wapi = WAPI(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_instantiate_wapi_with_dictionary_of_arguments():
    props = dict(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi = WAPI(**props)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_ssl_verify_as_string_value():
    wapi = WAPI(ssl_verify='/path/to/certfile')
    assert isinstance(wapi.ssl_verify, str)
    assert wapi.ssl_verify == '/path/to/certfile'


def test_ssl_verify_as_boolean_value():
    wapi = WAPI(ssl_verify=False)
    assert isinstance(wapi.ssl_verify, bool)
    assert wapi.ssl_verify is False


def test_wapi_basic_auth_connection():
    wapi = WAPI(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi.connect(username=USERNAME, password=PASSWORD)
    assert wapi.grid_ref is not None


def test_wapi_basic_auth_connection_with_bad_password():
    wapi = WAPI(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    try:
        wapi.connect(username=USERNAME, password='bad_password')
    except WapiRequestException as err:
        assert '401 Client Error: Authorization Required' in str(err)
    assert wapi.grid_ref is None
