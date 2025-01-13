# File: tests/test_dhcp.py

from ipaddress import IPv4Address
from logging import getLogger

import pytest

from src.ibx_sdk.nios.csv.dhcp import IPv4Network
from src.ibx_sdk.nios.csv.enums import ImportActionEnum

LOG = getLogger(__name__)


def test_ipv4network_creation_with_valid_data():
    data = {
        "import_action": ImportActionEnum.INSERT_OVERRIDE,
        "address": IPv4Address("192.168.1.0"),
        "netmask": IPv4Address("255.255.255.0"),
    }
    ipv4_network = IPv4Network(**data)

    assert ipv4_network.import_action == ImportActionEnum.INSERT_OVERRIDE
    assert ipv4_network.address == IPv4Address("192.168.1.0")
    assert ipv4_network.netmask == IPv4Address("255.255.255.0")


def test_ipv4network_creation_with_optional_fields():
    data = {
        "address": IPv4Address("10.0.0.0"),
        "netmask": IPv4Address("255.0.0.0"),
        "rir_organization": "RIR Org",
        "enable_discovery": True,
        "discovery_member": "Member1",
    }
    ipv4_network = IPv4Network(**data)

    assert ipv4_network.rir_organization == "RIR Org"
    assert ipv4_network.enable_discovery is True
    assert ipv4_network.discovery_member == "Member1"


def test_ipv4network_invalid_address():
    data = {
        "address": "invalid_ip",
        "netmask": IPv4Address("255.255.255.0"),
    }
    with pytest.raises(ValueError):
        IPv4Network(**data)


def test_ipv4network_add_property_valid_code():
    data = {
        "address": IPv4Address("192.168.1.0"),
        "netmask": IPv4Address("255.255.255.0"),
    }
    ipv4_network = IPv4Network(**data)

    ipv4_network.add_property("OPTION-1", "Test Option")
    assert getattr(ipv4_network, "OPTION-1") == "Test Option"


def test_ipv4network_add_property_invalid_code():
    data = {
        "address": IPv4Address("192.168.1.0"),
        "netmask": IPv4Address("255.255.255.0"),
    }
    ipv4_network = IPv4Network(**data)

    with pytest.raises(Exception, match="Invalid field name: INVALID-CODE"):
        ipv4_network.add_property("INVALID-CODE", "Test Value")
