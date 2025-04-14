import pytest
from pydantic import ValidationError

from src.ibx_sdk.nios.csv.dhcp import IPv4SharedNetwork
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_ipv4sharednetwork_default_values():
    shared_network = IPv4SharedNetwork(
        name="test_network",
        networks=["192.168.0.0/24", "192.168.1.0/24", "192.168.2.0/24"],
    )
    assert shared_network.sharednetwork == "sharednetwork"
    assert shared_network.name == "test_network"
    assert shared_network.networks == [
        "192.168.0.0/24",
        "192.168.1.0/24",
        "192.168.2.0/24",
    ]
    assert shared_network.import_action is None
    assert shared_network.new_name is None
    assert shared_network.network_view is None
    assert shared_network.comment is None


def test_ipv4sharednetwork_with_all_fields():
    shared_network = IPv4SharedNetwork(
        name="test_network",
        networks=["192.168.0.0/24", "192.168.1.0/24", "192.168.2.0/24"],
        network_view="default",
        import_action=ImportActionEnum.INSERT,
        new_name="test_network_new",
        comment="This is a test comment",
        is_authoritative=True,
        option_logic_filters=["filter1", "filter2"],
        boot_file="bootfile.cfg",
        boot_server="bootserver",
        generate_hostname=True,
        always_update_dns=True,
        update_static_leases=False,
        update_dns_on_lease_renewal=True,
        ddns_ttl=3600,
        enable_option81=True,
        deny_bootp=False,
        disabled=False,
        enable_ddns=True,
        ignore_client_requested_options=True,
        next_server="192.168.0.1",
        lease_time=7200,
        enable_pxe_lease_time=True,
        pxe_lease_time=3600,
        routers="192.168.0.1",
        domain_name="example.com",
        domain_name_servers="8.8.8.8,8.8.4.4",
    )
    assert shared_network.network_view == "default"
    assert shared_network.import_action == ImportActionEnum.INSERT
    assert shared_network.new_name == "test_network_new"
    assert shared_network.comment == "This is a test comment"
    assert shared_network.is_authoritative is True
    assert shared_network.option_logic_filters == ["filter1", "filter2"]
    assert shared_network.boot_file == "bootfile.cfg"
    assert shared_network.boot_server == "bootserver"
    assert shared_network.generate_hostname is True
    assert shared_network.always_update_dns is True
    assert shared_network.update_static_leases is False
    assert shared_network.update_dns_on_lease_renewal is True
    assert shared_network.ddns_ttl == 3600
    assert shared_network.enable_option81 is True
    assert shared_network.deny_bootp is False
    assert shared_network.disabled is False
    assert shared_network.enable_ddns is True
    assert shared_network.ignore_client_requested_options is True
    assert shared_network.next_server == "192.168.0.1"
    assert shared_network.lease_time == 7200
    assert shared_network.enable_pxe_lease_time is True
    assert shared_network.pxe_lease_time == 3600
    assert shared_network.routers == "192.168.0.1"
    assert shared_network.domain_name == "example.com"
    assert shared_network.domain_name_servers == "8.8.8.8,8.8.4.4"


def test_ipv4sharednetwork_missing_required_fields():
    with pytest.raises(ValidationError):
        IPv4SharedNetwork()


def test_ipv4sharednetwork_invalid_field_name_in_add_property():
    shared_network = IPv4SharedNetwork(name="test_network", networks=["192.168.0.0/24"])
    with pytest.raises(Exception, match="Invalid field name: INVALID-FIELD"):
        shared_network.add_property("INVALID-FIELD", "value")


def test_ipv4sharednetwork_valid_field_name_in_add_property():
    shared_network = IPv4SharedNetwork(name="test_network", networks=["192.168.0.0/24"])
    shared_network.add_property("OPTION-TestOption", "SomeValue")
    assert getattr(shared_network, "OPTION-TestOption") == "SomeValue"
