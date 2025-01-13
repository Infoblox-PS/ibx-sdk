# File: tests/test_dhcp.py

from ipaddress import IPv4Address

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv4FixedAddress
from src.ibx_sdk.nios.csv.enums import ImportActionEnum, MatchOptionEnum


def test_ipv4fixedaddress_default_values():
    ipv4_fixed_address = IPv4FixedAddress(ip_address=IPv4Address("192.168.1.1"))
    assert ipv4_fixed_address.header_fixedaddress == "fixedaddress"
    assert ipv4_fixed_address.import_action is None
    assert ipv4_fixed_address.ip_address == IPv4Address("192.168.1.1")
    assert ipv4_fixed_address.ms_server is None
    assert ipv4_fixed_address.new_ip_address is None
    assert ipv4_fixed_address.network_view is None
    assert ipv4_fixed_address.name is None
    assert ipv4_fixed_address.always_update_dns is None
    assert ipv4_fixed_address.option_logic_filters is None
    assert ipv4_fixed_address.boot_file is None
    assert ipv4_fixed_address.boot_server is None
    assert ipv4_fixed_address.prepared_zero is None
    assert ipv4_fixed_address.comment is None
    assert ipv4_fixed_address.ddns_domainname is None
    assert ipv4_fixed_address.deny_bootp is None
    assert ipv4_fixed_address.broadcast_address is None
    assert ipv4_fixed_address.routers is None
    assert ipv4_fixed_address.domain_name is None
    assert ipv4_fixed_address.domain_name_servers is None
    assert ipv4_fixed_address.dhcp_client_identifier is None
    assert ipv4_fixed_address.disabled is None
    assert ipv4_fixed_address.enable_ddns is None
    assert ipv4_fixed_address.ignore_client_requested_options is None
    assert ipv4_fixed_address.circuit_id is None
    assert ipv4_fixed_address.remote_id is None
    assert ipv4_fixed_address.mac_address is None
    assert ipv4_fixed_address.match_option is None
    assert ipv4_fixed_address.next_server is None
    assert ipv4_fixed_address.lease_time is None
    assert ipv4_fixed_address.enable_pxe_lease_time is None
    assert ipv4_fixed_address.ddns_hostname is None
    assert ipv4_fixed_address.pxe_lease_time is None


def test_ipv4fixedaddress_invalid_ip_address():
    with pytest.raises(ValidationError):
        IPv4FixedAddress(ip_address="invalid-ip")


def test_ipv4fixedaddress_import_action_enum():
    ipv4_fixed_address = IPv4FixedAddress(
        ip_address=IPv4Address("192.168.1.1"),
        import_action=ImportActionEnum.INSERT,
    )
    assert ipv4_fixed_address.import_action == ImportActionEnum.INSERT


def test_ipv4fixedaddress_match_option_enum():
    ipv4_fixed_address = IPv4FixedAddress(
        ip_address=IPv4Address("192.168.1.1"),
        match_option=MatchOptionEnum.MAC_ADDRESS,
    )
    assert ipv4_fixed_address.match_option == MatchOptionEnum.MAC_ADDRESS


def test_ipv4fixedaddress_add_property_valid_field():
    ipv4_fixed_address = IPv4FixedAddress(ip_address=IPv4Address("192.168.1.1"))
    ipv4_fixed_address.add_property("OPTION-custom", "value")
    assert getattr(ipv4_fixed_address, "OPTION-custom") == "value"


def test_ipv4fixedaddress_add_property_invalid_field():
    ipv4_fixed_address = IPv4FixedAddress(ip_address=IPv4Address("192.168.1.1"))
    with pytest.raises(Exception, match="Invalid field name"):
        ipv4_fixed_address.add_property("INVALID-OPTION", "value")
