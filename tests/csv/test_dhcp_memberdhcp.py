from ipaddress import IPv4Address
from logging import getLogger
import pytest
from pydantic import PositiveInt, ValidationError
from src.ibx_sdk.nios.csv.dhcp import MemberDhcp
from src.ibx_sdk.nios.csv.enums import ImportActionEnum

LOG = getLogger(__name__)


def test_memberdhcp_default_initialization():
    member_dhcp = MemberDhcp(name="TestDHCP")
    assert member_dhcp.name == "TestDHCP"
    assert member_dhcp.memberdhcp == "memberdhcp"


def test_memberdhcp_with_optional_fields():
    member_dhcp = MemberDhcp(
        name="TestDHCP",
        import_action=ImportActionEnum.INSERT,
        broadcast_address=IPv4Address("192.168.1.255"),
        lease_time=PositiveInt(3600),
        ping_count=PositiveInt(2),
    )
    assert member_dhcp.broadcast_address == IPv4Address("192.168.1.255")
    assert member_dhcp.lease_time == 3600
    assert member_dhcp.ping_count == 2
    assert member_dhcp.import_action == ImportActionEnum.INSERT


def test_memberdhcp_invalid_broadcast_address():
    with pytest.raises(ValidationError):
        MemberDhcp(name="TestDHCP", broadcast_address="invalid_ip")


def test_memberdhcp_invalid_positiveint_field():
    with pytest.raises(ValidationError):
        MemberDhcp(name="TestDHCP", lease_time=-100)


def test_memberdhcp_add_property_valid():
    member_dhcp = MemberDhcp(name="TestDHCP")
    member_dhcp.add_property(code="OPTION-Test", value="Value1")
    assert getattr(member_dhcp, "OPTION-Test") == "Value1"


def test_memberdhcp_add_property_invalid():
    member_dhcp = MemberDhcp(name="TestDHCP")
    with pytest.raises(Exception) as exc:
        member_dhcp.add_property(code="INVALID-Test", value="Value1")
    assert "Invalid field name" in str(exc.value)


def test_memberdhcp_ddns_fields():
    member_dhcp = MemberDhcp(
        name="TestDHCP",
        enable_ddns=True,
        ddns_use_option81=True,
        ddns_ttl=PositiveInt(3600),
        ddns_domainname="example.com",
    )
    assert member_dhcp.enable_ddns is True
    assert member_dhcp.ddns_use_option81 is True
    assert member_dhcp.ddns_ttl == 3600
    assert member_dhcp.ddns_domainname == "example.com"


def test_memberdhcp_ipv6_fields():
    member_dhcp = MemberDhcp(
        name="TestDHCP",
        ipv6_enable_ddns=True,
        ipv6_domain_name="example.com",
        ipv6_ddns_ttl=PositiveInt(3600),
    )
    assert member_dhcp.ipv6_enable_ddns is True
    assert member_dhcp.ipv6_domain_name == "example.com"
    assert member_dhcp.ipv6_ddns_ttl == 3600


def test_memberdhcp_invalid_enum():
    with pytest.raises(ValidationError):
        MemberDhcp(name="TestDHCP", leases_per_client_settings="INVALID_ENUM")
