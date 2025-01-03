# File: tests/test_dhcp.py

from logging import getLogger
from ipaddress import IPv4Address

import pytest
from src.ibx_sdk.nios.csv.dhcp import IPv4NetworkContainer
from src.ibx_sdk.nios.csv.enums import ImportActionEnum
LOG = getLogger(__name__)


def test_ipv4networkcontainer_mandatory_fields():
    # Test object creation with only mandatory fields
    container = IPv4NetworkContainer(
        address=IPv4Address("192.168.0.1"),
        netmask=IPv4Address("255.255.255.0")
    )
    assert container.address == IPv4Address("192.168.0.1")
    assert container.netmask == IPv4Address("255.255.255.0")
    assert container.networkcontainer == "networkcontainer"


def test_ipv4networkcontainer_optional_fields():
    # Test object creation with all fields specified
    container = IPv4NetworkContainer(
        address=IPv4Address("10.0.0.1"),
        netmask=IPv4Address("255.255.255.0"),
        comment="Test container",
        lease_time=3600,
        domain_name="example.com",
        enable_ddns=True
    )
    assert container.comment == "Test container"
    assert container.lease_time == 3600
    assert container.domain_name == "example.com"
    assert container.enable_ddns is True


def test_ipv4networkcontainer_invalid_field_exception():
    # Test exception for invalid field added via add_property
    container = IPv4NetworkContainer(
        address=IPv4Address("192.168.1.0"),
        netmask=IPv4Address("255.255.255.0")
    )
    with pytest.raises(Exception, match="Invalid field name: INVALID-FIELD"):
        container.add_property("INVALID-FIELD", "value")


def test_ipv4networkcontainer_valid_custom_field():
    # Test adding valid custom field via add_property
    container = IPv4NetworkContainer(
        address=IPv4Address("10.0.0.1"),
        netmask=IPv4Address("255.255.255.0")
    )
    container.add_property("OPTION-123", "sample-value")
    model = container.model_dump(exclude_none=True, exclude_unset=True, by_alias=False)
    assert model.get('OPTION-123') == "sample-value"


def test_ipv4networkcontainer_import_action():
    # Test creation with valid enum value for import_action
    container = IPv4NetworkContainer(
        address=IPv4Address("192.168.1.1"),
        netmask=IPv4Address("255.255.255.0"),
        import_action=ImportActionEnum.INSERT
    )
    model = container.model_dump(exclude_none=True, exclude_unset=True, by_alias=False)
    # LOG.info(model)
    # LOG.info(container.import_action)
    # LOG.info(container.model_fields['import_action'])
    assert model.get('import_action') == ImportActionEnum.INSERT


def test_ipv4networkcontainer_invalid_address():
    # Test invalid IP address for the address field
    with pytest.raises(ValueError):
        IPv4NetworkContainer(
            address="invalid-ip",
            netmask=IPv4Address("255.255.255.0")
        )


def test_ipv4networkcontainer_invalid_netmask():
    # Test invalid IP address for the netmask field
    with pytest.raises(ValueError):
        IPv4NetworkContainer(
            address=IPv4Address("192.168.1.1"),
            netmask="invalid-netmask"
        )
