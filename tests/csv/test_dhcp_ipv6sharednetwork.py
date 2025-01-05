import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import IPv6SharedNetwork


def test_ipv6sharednetwork_default_values():
    ipv6_shared_network = IPv6SharedNetwork(
        name="test_shared_network",
        networks=["2001:db8::/32", "2001:db8:1::/64"]
    )
    assert ipv6_shared_network.ipv6sharednetwork == "ipv6sharednetwork"
    assert ipv6_shared_network.import_action is None
    assert ipv6_shared_network.name == "test_shared_network"
    assert ipv6_shared_network.new_name is None
    assert ipv6_shared_network.networks == ["2001:db8::/32", "2001:db8:1::/64"]
    assert ipv6_shared_network.network_view is None
    assert ipv6_shared_network.comment is None
    assert ipv6_shared_network.disabled is None
    assert ipv6_shared_network.domain_name is None
    assert ipv6_shared_network.domain_name_servers is None
    assert ipv6_shared_network.valid_lifetime is None
    assert ipv6_shared_network.preferred_lifetime is None
    assert ipv6_shared_network.enable_ddns is None
    assert ipv6_shared_network.always_update_dns is None
    assert ipv6_shared_network.ddns_domain_name is None
    assert ipv6_shared_network.ddns_ttl is None
    assert ipv6_shared_network.generate_hostname is None
    assert ipv6_shared_network.update_dns_on_lease_renewal is None


def test_ipv6sharednetwork_required_fields():
    with pytest.raises(ValidationError):
        IPv6SharedNetwork(networks=["2001:db8::/32"])  # Missing 'name'


def test_ipv6sharednetwork_valid_lifetime():
    ipv6_shared_network = IPv6SharedNetwork(
        name="test_shared_network",
        networks=["2001:db8::/32"],
        valid_lifetime=3600
    )
    assert ipv6_shared_network.valid_lifetime == 3600


def test_ipv6sharednetwork_invalid_lifetime():
    with pytest.raises(ValidationError):
        IPv6SharedNetwork(
            name="test_shared_network",
            networks=["2001:db8::/32"],
            valid_lifetime=-5  # Invalid value
        )


def test_ipv6sharednetwork_add_valid_property():
    ipv6_shared_network = IPv6SharedNetwork(
        name="test_shared_network",
        networks=["2001:db8::/32"]
    )
    ipv6_shared_network.add_property("OPTION-CODE1", "value1")
    assert getattr(ipv6_shared_network, "OPTION-CODE1") == "value1"


def test_ipv6sharednetwork_add_invalid_property():
    ipv6_shared_network = IPv6SharedNetwork(
        name="test_shared_network",
        networks=["2001:db8::/32"]
    )
    with pytest.raises(Exception, match="Invalid field name: INVALID-CODE"):
        ipv6_shared_network.add_property("INVALID-CODE", "value1")
