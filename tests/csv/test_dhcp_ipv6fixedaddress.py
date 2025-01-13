from ipaddress import IPv6Address

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv6FixedAddress
from src.ibx_sdk.nios.csv.enums import IPv6AddressTypeEnum, ImportActionEnum


def test_ipv6fixedaddress_default_values():
    ipv6_fixed_address = IPv6FixedAddress(
        ip_address=IPv6Address("2001:db8::1"),
        duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38"
    )
    assert ipv6_fixed_address.ipv6fixedaddress == "ipv6fixedaddress"
    assert ipv6_fixed_address.import_action is None
    assert ipv6_fixed_address.address_type is None
    assert ipv6_fixed_address.parent is None
    assert ipv6_fixed_address.ip_address == IPv6Address("2001:db8::1")
    assert ipv6_fixed_address.new_ip_address is None
    assert ipv6_fixed_address.ipv6_prefix is None
    assert ipv6_fixed_address.new_ipv6_prefix is None
    assert ipv6_fixed_address.ipv6_prefix_bits is None
    assert ipv6_fixed_address.new_ipv6_prefix_bits is None
    assert ipv6_fixed_address.network_view is None
    assert ipv6_fixed_address.name is None
    assert ipv6_fixed_address.comment is None
    assert ipv6_fixed_address.disabled is None
    assert ipv6_fixed_address.match_option == "DUID"
    assert ipv6_fixed_address.duid == "00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38"
    assert ipv6_fixed_address.domain_name is None
    assert ipv6_fixed_address.domain_name_servers is None
    assert ipv6_fixed_address.valid_lifetime is None
    assert ipv6_fixed_address.preferred_lifetime is None


def test_ipv6fixedaddress_with_custom_values():
    ipv6_fixed_address = IPv6FixedAddress(
        ip_address=IPv6Address("2001:db8::1"),
        duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38",
        import_action=ImportActionEnum.INSERT,
        address_type=IPv6AddressTypeEnum.ADDRESS,
        network_view="default",
        name="test_fixed_address",
        comment="Test comment",
        disabled=True,
        match_option="MAC",
        domain_name="example.com",
        domain_name_servers="2001:4860:4860::8888",
        valid_lifetime=86400,
        preferred_lifetime=43200
    )
    assert ipv6_fixed_address.import_action == ImportActionEnum.INSERT
    assert ipv6_fixed_address.address_type == IPv6AddressTypeEnum.ADDRESS
    assert ipv6_fixed_address.network_view == "default"
    assert ipv6_fixed_address.name == "test_fixed_address"
    assert ipv6_fixed_address.comment == "Test comment"
    assert ipv6_fixed_address.disabled is True
    assert ipv6_fixed_address.match_option == "MAC"
    assert ipv6_fixed_address.domain_name == "example.com"
    assert ipv6_fixed_address.domain_name_servers == "2001:4860:4860::8888"
    assert ipv6_fixed_address.valid_lifetime == 86400
    assert ipv6_fixed_address.preferred_lifetime == 43200


def test_ipv6fixedaddress_invalid_ip_address():
    with pytest.raises(ValidationError):
        IPv6FixedAddress(
            ip_address="invalid-ip",
            duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38"
        )


def test_ipv6fixedaddress_invalid_prefix():
    with pytest.raises(ValidationError):
        IPv6FixedAddress(
            ip_address=IPv6Address("2001:db8::1"),
            duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38",
            ipv6_prefix=129
        )


def test_ipv6fixedaddress_add_property_valid():
    ipv6_fixed_address = IPv6FixedAddress(
        ip_address=IPv6Address("2001:db8::1"),
        duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38"
    )
    ipv6_fixed_address.add_property("OPTION-customer-vlan", "1001")
    assert getattr(ipv6_fixed_address, "OPTION-customer-vlan") == "1001"


def test_ipv6fixedaddress_add_property_invalid():
    ipv6_fixed_address = IPv6FixedAddress(
        ip_address=IPv6Address("2001:db8::1"),
        duid="00:01:00:01:1c:71:7a:64:00:0c:29:56:0e:38"
    )
    with pytest.raises(Exception, match="Invalid field name"):
        ipv6_fixed_address.add_property("INVALID-property", "xyz")
