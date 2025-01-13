import pytest
from pydantic import ValidationError

from src.ibx_sdk.nios.csv.dhcp import GridDhcp
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_griddhcp_default_values():
    griddhcp = GridDhcp()
    assert griddhcp.griddhcp == "griddhcp"
    assert griddhcp.authority is None
    assert griddhcp.domain_name is None


def test_griddhcp_create_with_valid_values():
    data = {
        "authority": True,
        "domain_name": "example.com",
        "recycle_leases": False,
        "pxe_lease_time": 300,
    }
    griddhcp = GridDhcp(**data)
    assert griddhcp.authority is True
    assert griddhcp.domain_name == "example.com"
    assert griddhcp.recycle_leases is False
    assert griddhcp.pxe_lease_time == 300


def test_griddhcp_override_values():
    griddhcp = GridDhcp(
        authority=False,
        domain_name="other.com",
        recycle_leases=True,
        pxe_lease_time=600,
        import_action=ImportActionEnum.OVERRIDE
    )
    assert griddhcp.authority is False
    assert griddhcp.domain_name == "other.com"
    assert griddhcp.recycle_leases is True
    assert griddhcp.pxe_lease_time == 600
    assert griddhcp.import_action == ImportActionEnum.OVERRIDE


def test_griddhcp_invalid_pxe_lease_time():
    with pytest.raises(ValidationError):
        GridDhcp(pxe_lease_time=-1)


def test_griddhcp_optional_fields():
    data = {
        "domain_name": "test.com",
        "ddns_ttl": 600,
        "email_list": "admin@test.com",
        "ipv6_domain_name": "ipv6-test.com",
        "ignore_client_identifier": True,
    }
    griddhcp = GridDhcp(**data)
    assert griddhcp.domain_name == "test.com"
    assert griddhcp.ddns_ttl == 600
    assert griddhcp.email_list == "admin@test.com"
    assert griddhcp.ipv6_domain_name == "ipv6-test.com"
    assert griddhcp.ignore_client_identifier is True


def test_griddhcp_add_property_valid():
    griddhcp = GridDhcp()
    griddhcp.add_property("OPTION-DUMMY", "dummy_value")
    assert getattr(griddhcp, "OPTION-DUMMY") == "dummy_value"


def test_griddhcp_add_property_invalid_code():
    griddhcp = GridDhcp()
    with pytest.raises(Exception, match="Invalid field name: INVALID-OPTION"):
        griddhcp.add_property("INVALID-OPTION", "value")
