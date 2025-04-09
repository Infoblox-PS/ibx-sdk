# File: tests/test_dns.py
from logging import getLogger

import pytest
from pydantic import ValidationError

from ibx_sdk.nios.csv.dns import MemberDns
from ibx_sdk.nios.csv.enums import ImportActionEnum

LOG = getLogger(__name__)


def test_memberdns_default_values():
    member_dns = MemberDns(parent="example.com")
    assert member_dns.memberdns == "memberdns"
    assert member_dns.import_action is None
    assert member_dns.parent == "example.com"
    assert member_dns.dns_over_mgmt is None
    assert member_dns.dns_over_lan2 is None
    assert member_dns.minimal_response is None
    assert member_dns.forwarders_only is None
    assert member_dns.allow_forwarder is None
    assert member_dns.member_view_nats is None


def test_memberdns_with_optional_fields():
    member_dns = MemberDns(
        parent="example.com",
        import_action=ImportActionEnum.OVERRIDE,
        dns_over_mgmt=True,
        minimal_response=False,
        notify_source_port=53,
    )
    assert member_dns.parent == "example.com"
    assert member_dns.import_action == ImportActionEnum.OVERRIDE
    assert member_dns.dns_over_mgmt is True
    assert member_dns.minimal_response is False
    assert member_dns.notify_source_port == 53


def test_memberdns_invalid_parent():
    with pytest.raises(ValidationError):
        MemberDns(parent=None)


def test_memberdns_lame_ttl_out_of_range():
    member_dns = MemberDns(parent="example.com", lame_ttl=4)
    assert member_dns.lame_ttl == 4
    with pytest.raises(ValidationError):
        MemberDns(parent="example.com", lame_ttl=86401)


def test_memberdns_allow_forwarder_list():
    member_dns = MemberDns(
        parent="example.com",
        allow_forwarder=["192.168.1.1", "10.0.0.1"],
    )
    assert member_dns.allow_forwarder == [
        "192.168.1.1",
        "10.0.0.1",
    ]


def test_memberdns_notify_delay_limits():
    with pytest.raises(ValidationError):
        MemberDns(parent="example.com", notify_delay=4)
    with pytest.raises(ValidationError):
        MemberDns(parent="example.com", notify_delay=86401)
    member_dns = MemberDns(parent="example.com", notify_delay=3600)
    assert member_dns.notify_delay == 3600


def test_memberdns_concurrent_recursive_clients_default():
    member_dns = MemberDns(parent="example.com")
    assert member_dns.concurrent_recursive_clients == 1000


def test_memberdns_invalid_query_source_port():
    with pytest.raises(ValidationError):
        MemberDns(parent="ns1.example.com", query_source_port=0)
    with pytest.raises(ValidationError):
        MemberDns(parent="ns1.example.com", query_source_port=-1)


def test_memberdns_nxdomain_redirect_addresses():
    member_dns = MemberDns(
        parent="ns1.example.com",
        nxdomain_redirect_addresses=["192.0.2.1", "198.51.100.1"],
    )
    assert member_dns.nxdomain_redirect_addresses == [
        "192.0.2.1",
        "198.51.100.1",
    ]


def test_memberdns_blacklist_parameters():
    member_dns = MemberDns(
        parent="ns1.example.com",
        enable_blacklist=True,
        blacklist_redirect_addresses=[
            "203.0.113.1",
            "192.0.2.1",
            "2001:db8::1",
        ],
        blacklist_redirect_ttl=3600,
    )
    assert member_dns.enable_blacklist is True
    assert member_dns.blacklist_redirect_addresses == [
        "203.0.113.1",
        "192.0.2.1",
        "2001:db8::1",
    ]
    assert member_dns.blacklist_redirect_ttl == 3600
