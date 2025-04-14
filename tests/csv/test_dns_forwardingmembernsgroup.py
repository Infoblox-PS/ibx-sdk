import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import ForwardingMemberNsGroup
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_forwardingmembernsgroup_default_values():
    ns_group = ForwardingMemberNsGroup(group_name="DefaultGroup")
    assert ns_group.forwardingmembernsgroup == "forwardingmembernsgroup"
    assert ns_group.group_name == "DefaultGroup"
    assert ns_group.import_action is None
    assert ns_group.new_group_name is None
    assert ns_group.comment is None
    assert ns_group.forwarding_servers is None


def test_forwardingmembernsgroup_with_all_fields():
    ns_group = ForwardingMemberNsGroup(
        group_name="NSGroup1",
        import_action=ImportActionEnum.OVERRIDE,
        new_group_name="NewNSGroup",
        comment="This is a comment",
        forwarding_servers=["192.168.1.1", "example.com"],
    )
    assert ns_group.forwardingmembernsgroup == "forwardingmembernsgroup"
    assert ns_group.group_name == "NSGroup1"
    assert ns_group.import_action == ImportActionEnum.OVERRIDE
    assert ns_group.new_group_name == "NewNSGroup"
    assert ns_group.comment == "This is a comment"
    assert ns_group.forwarding_servers == ["192.168.1.1", "example.com"]


def test_serialize_forwarding_servers():
    ns_group = ForwardingMemberNsGroup(
        group_name="NSGroup1", forwarding_servers=["192.168.1.1", "example.com"]
    )
    serialized_value = ns_group.serialize_forwarding_servers(
        ns_group.forwarding_servers
    )
    assert serialized_value == "192.168.1.1,example.com"


def test_serialize_forwarding_servers_empty():
    ns_group = ForwardingMemberNsGroup(group_name="NSGroup1", forwarding_servers=[])
    serialized_value = ns_group.serialize_forwarding_servers(
        ns_group.forwarding_servers
    )
    assert serialized_value is None


def test_add_property_valid():
    ns_group = ForwardingMemberNsGroup(group_name="NSGroup1")
    ns_group.add_property("EA-CustomField", "Value123")
    assert getattr(ns_group, "EA-CustomField") == "Value123"


def test_add_property_invalid():
    ns_group = ForwardingMemberNsGroup(group_name="NSGroup1")
    with pytest.raises(Exception, match="Invalid field name: InvalidField"):
        ns_group.add_property("InvalidField", "Value123")


def test_forwardingmembernsgroup_missing_group_name():
    with pytest.raises(ValidationError):
        ForwardingMemberNsGroup()
