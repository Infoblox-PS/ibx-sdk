from ipaddress import IPv6Address

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv6Network
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_ipv6network_default_values():
    ipv6_network = IPv6Network(address=IPv6Address("::1"), cidr=64)
    assert ipv6_network.ipv6network == "ipv6network"
    assert ipv6_network.import_action is None
    assert ipv6_network.comment is None
    assert ipv6_network.network_view is None
    assert ipv6_network.enable_discovery is None
    assert ipv6_network.discovery_member is None
    assert ipv6_network.discovery_exclusion_range is None
    assert ipv6_network.disabled is None
    assert ipv6_network.auto_create_reversezone is None
    assert ipv6_network.zone_associations is None
    assert ipv6_network.dhcp_members is None
    assert ipv6_network.domain_name is None
    assert ipv6_network.domain_name_servers is None
    assert ipv6_network.valid_lifetime is None
    assert ipv6_network.preferred_lifetime is None
    assert ipv6_network.recycle_leases is None
    assert ipv6_network.enable_ddns is None
    assert ipv6_network.always_update_dns is None
    assert ipv6_network.ddns_domainname is None
    assert ipv6_network.ddns_ttl is None
    assert ipv6_network.generate_hostname is None
    assert ipv6_network.update_dns_on_lease_renewal is None
    assert ipv6_network.vlans is None
    assert ipv6_network.rir_organization is None
    assert ipv6_network.rir_registration_status is None


def test_ipv6network_with_all_fields():
    ipv6_network = IPv6Network(
        address=IPv6Address("2001:db8::"),
        cidr=48,
        import_action=ImportActionEnum.INSERT,
        comment="Test comment",
        network_view="default",
        enable_discovery=True,
        discovery_member="test_member",
        discovery_exclusion_range=[
            IPv6Address("2001:db8::1"),
            IPv6Address("2001:db8::2"),
        ],
        disabled=False,
        auto_create_reversezone=True,
        zone_associations=["zone1", "zone2"],
        dhcp_members="member1,member2",
        domain_name="example.com",
        domain_name_servers="8.8.8.8,8.8.4.4",
        valid_lifetime=3600,
        preferred_lifetime=1800,
        recycle_leases=True,
        enable_ddns=True,
        always_update_dns=False,
        ddns_domainname="ddns.example.com",
        ddns_ttl=300,
        generate_hostname=False,
        update_dns_on_lease_renewal=True,
        vlans="default/1",
        rir_organization="RIROrg",
        rir_registration_status="Registered",
    )
    assert ipv6_network.address == IPv6Address("2001:db8::")
    assert ipv6_network.cidr == 48
    assert ipv6_network.import_action == ImportActionEnum.INSERT
    assert ipv6_network.comment == "Test comment"
    assert ipv6_network.network_view == "default"
    assert ipv6_network.enable_discovery is True
    assert ipv6_network.discovery_member == "test_member"
    assert ipv6_network.discovery_exclusion_range == [
        IPv6Address("2001:db8::1"),
        IPv6Address("2001:db8::2"),
    ]
    assert ipv6_network.disabled is False
    assert ipv6_network.auto_create_reversezone is True
    assert ipv6_network.zone_associations == ["zone1", "zone2"]
    assert ipv6_network.dhcp_members == "member1,member2"
    assert ipv6_network.domain_name == "example.com"
    assert ipv6_network.domain_name_servers == "8.8.8.8,8.8.4.4"
    assert ipv6_network.valid_lifetime == 3600
    assert ipv6_network.preferred_lifetime == 1800
    assert ipv6_network.recycle_leases is True
    assert ipv6_network.enable_ddns is True
    assert ipv6_network.always_update_dns is False
    assert ipv6_network.ddns_domainname == "ddns.example.com"
    assert ipv6_network.ddns_ttl == 300
    assert ipv6_network.generate_hostname is False
    assert ipv6_network.update_dns_on_lease_renewal is True
    assert ipv6_network.vlans == "default/1"
    assert ipv6_network.rir_organization == "RIROrg"
    assert ipv6_network.rir_registration_status == "Registered"


def test_ipv6network_invalid_cidr_value():
    with pytest.raises(ValidationError):
        IPv6Network(address=IPv6Address("2001:db8::"), cidr=129)


def test_ipv6network_missing_required_fields():
    with pytest.raises(ValidationError):
        IPv6Network()


def test_add_property_valid():
    ipv6_network = IPv6Network(address=IPv6Address("2001:db8::"), cidr=48)
    ipv6_network.add_property("OPTION-test", "value")
    assert getattr(ipv6_network, "OPTION-test") == "value"


def test_add_property_invalid():
    ipv6_network = IPv6Network(address=IPv6Address("2001:db8::"), cidr=48)
    with pytest.raises(Exception, match="Invalid field name: invalid_code"):
        ipv6_network.add_property("invalid_code", "value")
