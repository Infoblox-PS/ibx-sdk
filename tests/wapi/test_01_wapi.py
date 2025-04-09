"""
WAPI test module
"""

import logging
import os

import pytest
import urllib3

from ibx_sdk.nios.exceptions import WapiInvalidParameterException, WapiRequestException
from ibx_sdk.nios.gift import Gift

log = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get("GRID_MGR")
WAPI_VER = os.environ.get("WAPI_VER")
PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")
SSL_VERIFY = False if os.environ.get("SSL_VERIFY") == "False" else True


def test_instantiate_wapi_without_properties():
    wapi = Gift()
    assert wapi.grid_mgr is None
    assert wapi.wapi_ver == "2.5"
    assert wapi.ssl_verify is False
    assert wapi.url == ""
    assert isinstance(wapi, Gift)


def test_instantiate_wapi_with_positional_arguments():
    wapi = Gift(GRID_MGR, WAPI_VER, SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_instantiate_wapi_with_named_arguments():
    wapi = Gift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_instantiate_wapi_with_dictionary_of_arguments():
    props = dict(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi = Gift(**props)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


def test_wapi_connect_with_bogus_server():
    wapi = Gift(grid_mgr="1.1.1.1")
    with pytest.raises(WapiRequestException):
        wapi.connect(username=USERNAME, password=PASSWORD)


def test_wapi_connect_with_invalid_url():
    wapi = Gift()
    with pytest.raises(WapiInvalidParameterException):
        wapi.connect(username=USERNAME, password=PASSWORD)


def test_wapi_connect_without_arguments():
    wapi = Gift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(WapiInvalidParameterException):
        wapi.connect()


def test_ssl_verify_as_string_value():
    wapi = Gift(ssl_verify="/path/to/certfile")
    assert isinstance(wapi.ssl_verify, str)
    assert wapi.ssl_verify == "/path/to/certfile"


def test_ssl_verify_as_boolean_value():
    wapi = Gift(ssl_verify=False)
    assert isinstance(wapi.ssl_verify, bool)
    assert wapi.ssl_verify is False


def test_wapi_repr_function(get_wapi):
    wapi = get_wapi
    res = wapi.__repr__()
    assert "grid_ref" in res


def test_wapi_basic_auth_connection():
    wapi = Gift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi.connect(username=USERNAME, password=PASSWORD)
    assert wapi.grid_ref is not None


def test_wapi_certificate_auth_cert_not_found():
    wapi = Gift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(OSError):
        wapi.connect(certificate="/path/to/certfile")


def test_wapi_basic_auth_connection_with_bad_password():
    wapi = Gift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(WapiRequestException):
        wapi.connect(username=USERNAME, password="bad_password")
    assert wapi.grid_ref is None


def test_wapi_returns_cookie_connection(get_wapi):
    wapi = get_wapi
    cookies = wapi.conn.cookies
    assert "ibapauth" in cookies.keys()


def test_wapi_get_invalid_object(get_wapi):
    wapi = get_wapi
    try:
        response = wapi.get("invalid_object")
        log.debug(response.json())
        assert response.status_code == 400
    except WapiRequestException as err:
        log.debug(err)


def test_wapi_try_find_and_remove_object(get_wapi):
    wapi = get_wapi
    response = wapi.get("record:a", params={"name": "test.example.com"})
    if response.status_code == 200:
        if len(response.json()) > 0:
            for record in response.json():
                reference = record.get("_ref")
                res = wapi.delete(reference)
                assert res.status_code == 200
        else:
            assert len(response.json()) == 0


def test_wapi_object_create(get_wapi):
    wapi = get_wapi
    response = wapi.post(
        "record:a", json={"name": "test.example.com", "ipv4addr": "192.0.2.1"}
    )
    assert response.status_code == 201


def test_wapi_object_get(get_wapi):
    wapi = get_wapi
    response = wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_wapi_object_update(get_wapi):
    wapi = get_wapi
    response = wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    if len(response.json()) > 0:
        first_record = response.json()[0]
        reference = first_record.get("_ref")
        res = wapi.put(reference, json={"comment": "test update to comment"})
        assert res.status_code == 200


def test_wapi_object_delete(get_wapi):
    wapi = get_wapi
    response = wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    if len(response.json()) > 0:
        first_record = response.json()[0]
        reference = first_record.get("_ref")
        res = wapi.get(reference)
        assert res.status_code == 200
        _ref = wapi.delete(reference)
        assert _ref.json() == reference


def test_wapi_getone_success(get_wapi):
    wapi = get_wapi
    response = wapi.getone("grid")
    assert isinstance(response, str)


def test_wapi_getone_multiple(get_wapi):
    wapi = get_wapi
    with pytest.raises(WapiRequestException) as err:
        wapi.getone("network")
        assert err == "Multiple data records were returned"


def test_wapi_getone_no_data(get_wapi):
    wapi = get_wapi
    with pytest.raises(WapiRequestException) as err:
        wapi.getone("grid", params={"name": "does not exist"})
        assert err == "No data was returned"


def test_wapi_object_fields(get_wapi):
    wapi = get_wapi
    response = wapi.object_fields("grid")
    assert isinstance(response, str)


def test_wapi_max_version(get_wapi):
    wapi = get_wapi
    wapi.max_wapi_ver()
    assert wapi.wapi_ver != "1.0"
