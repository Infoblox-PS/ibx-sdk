"""
WAPI test module
"""

import logging
import os

import httpx
import pytest
import urllib3

from rich.console import Console
from ibx_sdk.nios.exceptions import WapiInvalidParameterException, WapiRequestException
from ibx_sdk.nios.asynchronous.gift import AsyncGift

log = logging.getLogger(__name__)
console = Console()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
GRID_MGR = os.environ.get("GRID_MGR")
WAPI_VER = os.environ.get("WAPI_VER")
PASSWORD = os.environ.get("PASSWORD")
USERNAME = os.environ.get("USERNAME")
SSL_VERIFY = False if os.environ.get("SSL_VERIFY") == "False" else True


@pytest.mark.asyncio
async def test_instantiate_wapi_without_properties():
    wapi = AsyncGift()
    assert wapi.grid_mgr is None
    assert wapi.wapi_ver == "2.5"
    assert wapi.ssl_verify is False
    assert wapi.url == ""
    assert isinstance(wapi, AsyncGift)


@pytest.mark.asyncio
async def test_instantiate_wapi_with_positional_arguments():
    wapi = AsyncGift(GRID_MGR, WAPI_VER, SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


@pytest.mark.asyncio
async def test_instantiate_wapi_with_named_arguments():
    wapi = AsyncGift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


@pytest.mark.asyncio
async def test_instantiate_wapi_with_dictionary_of_arguments():
    props = dict(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    wapi = AsyncGift(**props)
    assert wapi.grid_mgr == GRID_MGR
    assert wapi.wapi_ver == WAPI_VER
    assert wapi.ssl_verify == SSL_VERIFY


@pytest.mark.asyncio
async def test_wapi_connect_with_bogus_server():
    wapi = AsyncGift(grid_mgr="1.1.1.1")
    with pytest.raises(WapiRequestException):
        await wapi.connect(username=USERNAME, password=PASSWORD)


@pytest.mark.asyncio
async def test_wapi_connect_with_invalid_url():
    wapi = AsyncGift()
    with pytest.raises(WapiInvalidParameterException):
        await wapi.connect(username=USERNAME, password=PASSWORD)

@pytest.mark.asyncio
async def test_wapi_connect_without_arguments():
    wapi = AsyncGift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(WapiInvalidParameterException):
        await wapi.connect()


@pytest.mark.asyncio
async def test_ssl_verify_as_string_value():
    wapi = AsyncGift(ssl_verify="/path/to/certfile")
    assert isinstance(wapi.ssl_verify, str)
    assert wapi.ssl_verify == "/path/to/certfile"


@pytest.mark.asyncio
async def test_ssl_verify_as_boolean_value():
    wapi = AsyncGift(ssl_verify=False)
    assert isinstance(wapi.ssl_verify, bool)
    assert wapi.ssl_verify is False


@pytest.mark.asyncio
async def test_wapi_repr_function(get_async_wapi):
    wapi = get_async_wapi
    res = wapi.__repr__()
    assert "grid_ref" in res
    assert wapi.grid_ref is not None


@pytest.mark.asyncio
async def test_wapi_basic_auth_connection():
    wapi = AsyncGift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    await wapi.connect(username=USERNAME, password=PASSWORD)
    assert wapi.grid_ref is not None


@pytest.mark.asyncio
async def test_wapi_certificate_auth_cert_not_found():
    wapi = AsyncGift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(OSError):
        await wapi.connect(certificate="/path/to/certfile")


@pytest.mark.asyncio
async def test_wapi_basic_auth_connection_with_bad_password():
    wapi = AsyncGift(grid_mgr=GRID_MGR, wapi_ver=WAPI_VER, ssl_verify=SSL_VERIFY)
    with pytest.raises(WapiRequestException):
        await wapi.connect(username=USERNAME, password="bad_password")
    assert wapi.grid_ref is None


@pytest.mark.asyncio
async def test_wapi_returns_cookie_connection(get_async_wapi):
    wapi = get_async_wapi
    cookies = wapi.conn.cookies
    assert "ibapauth" in cookies.keys()


@pytest.mark.asyncio
async def test_wapi_get_invalid_object(get_async_wapi):
    wapi = get_async_wapi
    with pytest.raises(httpx.HTTPStatusError) as err:
        response = await wapi.get("invalid_object")
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_wapi_try_find_and_remove_object(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.get("record:a", params={"name": "test.example.com"})
    if response.status_code == 200:
        if len(response.json()) > 0:
            for record in response.json():
                reference = record.get("_ref")
                res = await wapi.delete(reference)
                assert res.status_code == 200
        else:
            assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_wapi_object_create(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.post(
        "record:a", json={"name": "test.example.com", "ipv4addr": "192.0.2.1"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_wapi_object_get(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_wapi_object_update(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    if len(response.json()) > 0:
        first_record = response.json()[0]
        reference = first_record.get("_ref")
        res = await wapi.put(reference, json={"comment": "test update to comment"})
        assert res.status_code == 200


@pytest.mark.asyncio
async def test_wapi_object_delete(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.get("record:a", params={"name": "test.example.com"})
    log.debug(response.json())
    if len(response.json()) > 0:
        first_record = response.json()[0]
        reference = first_record.get("_ref")
        res = await wapi.get(reference)
        assert res.status_code == 200
        _ref = await wapi.delete(reference)
        assert _ref.json() == reference


@pytest.mark.asyncio
async def test_wapi_getone_success(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.getone("grid")
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_wapi_getone_multiple(get_async_wapi):
    wapi = get_async_wapi
    with pytest.raises(WapiRequestException) as err:
        await wapi.getone("network")
        assert err == "Multiple data records were returned"


@pytest.mark.asyncio
async def test_wapi_getone_no_data(get_async_wapi):
    wapi = get_async_wapi
    with pytest.raises(WapiRequestException) as err:
        await wapi.getone("grid", params={"name": "does not exist"})
        assert err == "No data was returned"


@pytest.mark.asyncio
async def test_wapi_object_fields(get_async_wapi):
    wapi = get_async_wapi
    response = await wapi.object_fields("grid")
    assert isinstance(response, str)


@pytest.mark.asyncio
async def test_wapi_max_version(get_async_wapi):
    wapi = get_async_wapi
    await wapi.max_wapi_ver()
    assert wapi.wapi_ver != "1.0"
