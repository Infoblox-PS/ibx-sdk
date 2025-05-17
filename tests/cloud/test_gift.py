"""
test_gift.py

Unit tests for the Gift class.
"""

import pytest
from ibx_sdk.cloud.gift import Gift
from unittest.mock import patch, Mock
from pathlib import Path

@pytest.fixture
def gift_client(tmp_path):
    """
    Fixture to create a Gift client with a temporary cache file.
    """
    cache_file = tmp_path / "api_spec.json"
    return Gift(api_key="test_token", api_spec_file=str(cache_file), load_live=False)


def test_normalize_path(gift_client):
    """
    Test path normalization.
    """
    assert gift_client._normalize_path("/path/") == "path"
    assert gift_client._normalize_path("path/to/resource") == "path/to/resource"
    assert gift_client._normalize_path("///path//") == "path"


def test_resolve_endpoint(gift_client):
    """
    Test endpoint resolution for templated paths.
    """
    gift_client.api_data = {
        "NTPService GET /service/config/{id}": {
            "api": "NTPService",
            "method": "GET",
            "l_path": "/service/config/{id}",
            "s_path": "/service/config",
            "base_url": "https://csp.infoblox.com/api/ntp/v1",
            "summary": "Retrieve NTP configuration"
        }
    }
    gift_client.url_map = gift_client._build_url_map()

    url, meta, params = gift_client._resolve_endpoint("service/config/abc123", "GET")
    assert url == "https://csp.infoblox.com/api/ntp/v1/service/config/abc123"
    assert params == {"id": "abc123"}
    assert meta["api"] == "NTPService"


def test_resolve_endpoint_short_path(gift_client):
    """
    Test endpoint resolution for short paths.
    """
    gift_client.api_data = {
        "Locations GET /locations": {
            "api": "Locations",
            "method": "GET",
            "l_path": "/locations",
            "s_path": "/locations",
            "base_url": "https://csp.infoblox.com/api/infra/v1",
            "summary": "List locations"
        }
    }
    gift_client.url_map = gift_client._build_url_map()

    url, meta, params = gift_client._resolve_endpoint("locations", "GET")
    assert url == "https://csp.infoblox.com/api/infra/v1/locations"
    assert params is None
    assert meta["api"] == "Locations"


@patch("httpx.Client.get")
def test_get_call(mock_get, gift_client):
    """
    Test HTTP GET call.
    """
    mock_response = Mock()
    mock_response.json.return_value = {"result": []}
    mock_get.return_value = mock_response
    gift_client.connect()
    gift_client.api_data = {
        "Locations GET /locations": {
            "api": "Locations",
            "method": "GET",
            "l_path": "/locations",
            "s_path": "/locations",
            "base_url": "https://csp.infoblox.com/api/infra/v1",
            "summary": "List locations"
        }
    }
    gift_client.url_map = gift_client._build_url_map()

    response = gift_client.get("locations", params={"_limit": 10})
    assert response.json() == {"result": []}
    mock_get.assert_called_with("https://csp.infoblox.com/api/infra/v1/locations", params={"_limit": 10})


def test_find_endpoints(gift_client):
    """
    Test endpoint discovery.
    """
    gift_client.api_data = {
        "NTPService GET /service/config/{id}": {
            "api": "NTPService",
            "method": "GET",
            "l_path": "/service/config/{id}",
            "s_path": "/service/config",
            "base_url": "https://csp.infoblox.com/api/ntp/v1",
            "summary": "Retrieve NTP configuration"
        },
        "Locations GET /locations": {
            "api": "Locations",
            "method": "GET",
            "l_path": "/locations",
            "s_path": "/locations",
            "base_url": "https://csp.infoblox.com/api/infra/v1",
            "summary": "List locations"
        }
    }
    endpoints = gift_client.find_endpoints(api_name="NTPService", path_contains="service/config")
    assert len(endpoints) == 1
    assert endpoints[0]["path"] == "/service/config/{id}"
    assert endpoints[0]["api"] == "NTPService"


def test_context_manager(gift_client):
    """
    Test context manager for session management.
    """
    with gift_client as client:
        assert client.session is not None
    assert client.session is None