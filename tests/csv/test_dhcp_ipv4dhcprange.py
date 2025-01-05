# File: tests/test_dhcp.py

from ipaddress import IPv4Address

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv4DhcpRange
from src.ibx_sdk.nios.csv.enums import ImportActionEnum, ServerAssociationTypeEnum


def test_ipv4dhcprange_default_values():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("192.168.0.1"),
        end_address=IPv4Address("192.168.0.100")
    )
    assert ipv4_dhcp_range.dhcprange == "dhcprange"
    assert ipv4_dhcp_range.start_address == IPv4Address("192.168.0.1")
    assert ipv4_dhcp_range.end_address == IPv4Address("192.168.0.100")
    assert ipv4_dhcp_range.import_action is None
    assert ipv4_dhcp_range.new_start_address is None
    assert ipv4_dhcp_range.new_end_address is None
    assert ipv4_dhcp_range.network_view is None
    assert ipv4_dhcp_range.name is None
    assert ipv4_dhcp_range.comment is None
    assert ipv4_dhcp_range.is_authoritative is None


def test_ipv4dhcprange_custom_values():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("10.0.0.1"),
        end_address=IPv4Address("10.0.0.50"),
        name="Test DHCP Range",
        network_view="default",
        import_action=ImportActionEnum.INSERT_OVERRIDE,
        is_authoritative=True
    )
    assert ipv4_dhcp_range.start_address == IPv4Address("10.0.0.1")
    assert ipv4_dhcp_range.end_address == IPv4Address("10.0.0.50")
    assert ipv4_dhcp_range.name == "Test DHCP Range"
    assert ipv4_dhcp_range.network_view == "default"
    assert ipv4_dhcp_range.import_action == ImportActionEnum.INSERT_OVERRIDE
    assert ipv4_dhcp_range.is_authoritative is True


def test_ipv4dhcprange_invalid_start_address():
    with pytest.raises(ValidationError):
        IPv4DhcpRange(
            start_address="invalid-ip",
            end_address=IPv4Address("192.168.0.100")
        )


def test_ipv4dhcprange_invalid_end_address():
    with pytest.raises(ValidationError):
        IPv4DhcpRange(
            start_address=IPv4Address("192.168.0.1"),
            end_address="invalid-ip"
        )


def test_ipv4dhcprange_missing_end_address():
    with pytest.raises(ValidationError):
        IPv4DhcpRange(
            start_address=IPv4Address("192.168.0.1")
        )


def test_ipv4dhcprange_valid_range():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("192.168.0.1"),
        end_address=IPv4Address("192.168.0.100")
    )
    assert ipv4_dhcp_range.start_address == IPv4Address("192.168.0.1")
    assert ipv4_dhcp_range.end_address == IPv4Address("192.168.0.100")


def test_ipv4dhcprange_exclusion_ranges():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("192.168.1.1"),
        end_address=IPv4Address("192.168.1.100"),
        exclusion_ranges=["192.168.1.10-192.168.1.20"]
    )
    assert ipv4_dhcp_range.exclusion_ranges == ["192.168.1.10-192.168.1.20"]
    assert ipv4_dhcp_range.start_address == IPv4Address("192.168.1.1")
    assert ipv4_dhcp_range.end_address == IPv4Address("192.168.1.100")


def test_ipv4dhcprange_failover_association():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("10.0.0.1"),
        end_address=IPv4Address("10.0.0.100"),
        server_association_type=ServerAssociationTypeEnum.FAILOVER,
        failover_association="Test Failover"
    )
    assert ipv4_dhcp_range.server_association_type == ServerAssociationTypeEnum.FAILOVER
    assert ipv4_dhcp_range.failover_association == "Test Failover"


def test_ipv4dhcprange_add_property_valid():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("10.10.10.1"),
        end_address=IPv4Address("10.10.10.50")
    )
    ipv4_dhcp_range.add_property("OPTION-Custom1", "Custom Value")
    assert getattr(ipv4_dhcp_range, 'OPTION-Custom1') == "Custom Value"


def test_ipv4dhcprange_add_property_invalid():
    ipv4_dhcp_range = IPv4DhcpRange(
        start_address=IPv4Address("10.10.10.1"),
        end_address=IPv4Address("10.10.10.50")
    )
    with pytest.raises(Exception) as excinfo:
        ipv4_dhcp_range.add_property("InvalidCode", "Value")
    assert "Invalid field name: InvalidCode" in str(excinfo.value)
