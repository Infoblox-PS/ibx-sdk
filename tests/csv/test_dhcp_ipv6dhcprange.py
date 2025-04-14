from ipaddress import IPv6Address

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv6DhcpRange
from src.ibx_sdk.nios.csv.enums import IPv6AddressTypeEnum, ServerAssociationTypeEnum


def test_ipv6dhcprange_default_values():
    ipv6_dhcp_range = IPv6DhcpRange(
        start_address=IPv6Address("2001:db8::1"),
        end_address=IPv6Address("2001:db8::100"),
    )
    assert ipv6_dhcp_range.ipv6dhcprange == "ipv6dhcprange"
    assert ipv6_dhcp_range.import_action is None
    assert ipv6_dhcp_range.address_type is None
    assert ipv6_dhcp_range.parent is None
    assert ipv6_dhcp_range.start_address == IPv6Address("2001:db8::1")
    assert ipv6_dhcp_range.new_start_address is None
    assert ipv6_dhcp_range.end_address == IPv6Address("2001:db8::100")
    assert ipv6_dhcp_range.new_end_address is None
    assert ipv6_dhcp_range.ipv6_start_prefix is None
    assert ipv6_dhcp_range.new_ipv6_start_prefix is None
    assert ipv6_dhcp_range.ipv6_end_prefix is None
    assert ipv6_dhcp_range.new_ipv6_end_prefix is None
    assert ipv6_dhcp_range.ipv6_prefix_bits is None
    assert ipv6_dhcp_range.new_ipv6_prefix_bits is None
    assert ipv6_dhcp_range.network_view is None
    assert ipv6_dhcp_range.name is None
    assert ipv6_dhcp_range.comment is None
    assert ipv6_dhcp_range.disabled is None
    assert ipv6_dhcp_range.member is None
    assert ipv6_dhcp_range.server_association_type is None
    assert ipv6_dhcp_range.exclusion_ranges is None
    assert ipv6_dhcp_range.recycle_leases is None


def test_ipv6dhcprange_valid_values():
    ipv6_dhcp_range = IPv6DhcpRange(
        start_address=IPv6Address("2001:db8::1"),
        end_address=IPv6Address("2001:db8::100"),
        address_type=IPv6AddressTypeEnum.ADDRESS,
        network_view="default",
        name="range-01",
        disabled=False,
    )
    assert ipv6_dhcp_range.start_address == IPv6Address("2001:db8::1")
    assert ipv6_dhcp_range.end_address == IPv6Address("2001:db8::100")
    assert ipv6_dhcp_range.address_type == IPv6AddressTypeEnum.ADDRESS
    assert ipv6_dhcp_range.network_view == "default"
    assert ipv6_dhcp_range.name == "range-01"
    assert ipv6_dhcp_range.disabled is False


def test_ipv6dhcprange_invalid_start_address():
    with pytest.raises(ValidationError):
        IPv6DhcpRange(
            start_address="invalid-ip", end_address=IPv6Address("2001:db8::100")
        )


def test_ipv6dhcprange_invalid_end_address():
    with pytest.raises(ValidationError):
        IPv6DhcpRange(
            start_address=IPv6Address("2001:db8::1"), end_address="invalid-ip"
        )


def test_ipv6dhcprange_invalid_prefix():
    with pytest.raises(ValidationError):
        IPv6DhcpRange(
            start_address=IPv6Address("2001:db8::1"),
            end_address=IPv6Address("2001:db8::100"),
            ipv6_start_prefix=256,
        )


def test_ipv6dhcprange_exclusion_ranges():
    ipv6_dhcp_range = IPv6DhcpRange(
        start_address=IPv6Address("2001:db8::1"),
        end_address=IPv6Address("2001:db8::100"),
        exclusion_ranges=["2001:db8::10-2001:db8::20/comment"],
    )
    assert ipv6_dhcp_range.exclusion_ranges == ["2001:db8::10-2001:db8::20/comment"]


def test_ipv6dhcprange_server_association_type():
    ipv6_dhcp_range = IPv6DhcpRange(
        start_address=IPv6Address("2001:db8::1"),
        end_address=IPv6Address("2001:db8::100"),
        server_association_type=ServerAssociationTypeEnum.MEMBER,
    )
    assert ipv6_dhcp_range.server_association_type == ServerAssociationTypeEnum.MEMBER
