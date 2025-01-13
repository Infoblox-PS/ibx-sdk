from ipaddress import IPv6Address, IPv4Address

import pytest
from pydantic import ValidationError

from src.ibx_sdk.nios.csv.dhcp import IPv6NetworkContainer


def test_ipv6networkcontainer_default_values():
    container = IPv6NetworkContainer(address=IPv6Address("2001:db8::1"), cidr=48)
    assert container.import_action is None
    assert container.address == IPv6Address("2001:db8::1")
    assert container.network_view is None
    assert container.comment is None
    assert container.zone_associations is None
    assert container.valid_lifetime is None
    assert container.preferred_lifetime is None
    assert container.domain_name is None
    assert container.domain_name_servers is None
    assert container.recycle_leases is None
    assert container.enable_ddns is None
    assert container.ddns_domainname is None
    assert container.ddns_ttl is None
    assert container.generate_hostname is None
    assert container.always_update_dns is None
    assert container.update_dns_on_lease_renewal is None
    assert container.rir_organization is None
    assert container.rir_registration_status is None
    assert container.enable_discovery is None
    assert container.discovery_member is None
    assert container.discovery_exclusion_range is None
    assert container.remove_subnets is None


def test_ipv6networkcontainer_custom_values():
    container = IPv6NetworkContainer(
        address=IPv6Address("2001:db8::1"),
        cidr=48,
        network_view="default",
        comment="Test comment",
        valid_lifetime=3600,
        preferred_lifetime=1800,
        domain_name="example.com",
        recycle_leases=True,
    )
    assert container.cidr == 48
    assert container.network_view == "default"
    assert container.comment == "Test comment"
    assert container.valid_lifetime == 3600
    assert container.preferred_lifetime == 1800
    assert container.domain_name == "example.com"
    assert container.recycle_leases is True


def test_ipv6networkcontainer_invalid_address():
    with pytest.raises(ValidationError):
        IPv6NetworkContainer(address="192.168.1.1")


def test_ipv6networkcontainer_invalid_cidr():
    with pytest.raises(ValidationError):
        IPv6NetworkContainer(address=IPv6Address("2001:db8::1"), cidr=130)


def test_ipv6networkcontainer_add_property_valid():
    container = IPv6NetworkContainer(address=IPv6Address("2001:db8::1"), cidr=64)
    container.add_property("OPTION-Test", "Value")
    assert hasattr(container, "OPTION-Test")
    assert getattr(container, "OPTION-Test") == "Value"


def test_ipv6networkcontainer_add_property_invalid():
    container = IPv6NetworkContainer(address=IPv6Address("2001:db8::1"), cidr=64)
    with pytest.raises(Exception, match="Invalid field name: INVALID-Test"):
        container.add_property("INVALID-Test", "Value")


def test_ipv6networkcontainer_discovery_exclusion_range():
    container = IPv6NetworkContainer(
        address=IPv6Address("2001:db8::1"),
        cidr=64,
        discovery_exclusion_range=[IPv4Address("192.168.0.1"), IPv4Address("192.168.0.2")]
    )
    assert container.discovery_exclusion_range == [
        IPv4Address("192.168.0.1"),
        IPv4Address("192.168.0.2")
    ]
