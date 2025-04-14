import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import StubMemberNsGroup
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_stubmembernsgroup_default_values():
    ns_group = StubMemberNsGroup(group_name="DefaultGroup")
    assert ns_group.stubmembernsgroup == "stubmembernsgroup"
    assert ns_group.group_name == "DefaultGroup"
    assert ns_group.import_action is None
    assert ns_group.new_group_name is None
    assert ns_group.comment is None
    assert ns_group.stub_members is None


def test_stubmembernsgroup_with_all_fields():
    ns_group = StubMemberNsGroup(
        group_name="CustomGroup",
        import_action=ImportActionEnum.OVERRIDE,
        new_group_name="NewGroup",
        comment="This is a test comment",
        stub_members=["server1.example.com", "server2.example.com"],
    )
    assert ns_group.stubmembernsgroup == "stubmembernsgroup"
    assert ns_group.group_name == "CustomGroup"
    assert ns_group.import_action == ImportActionEnum.OVERRIDE
    assert ns_group.new_group_name == "NewGroup"
    assert ns_group.comment == "This is a test comment"
    assert ns_group.stub_members == ["server1.example.com", "server2.example.com"]


def test_stubmembernsgroup_invalid_group_name():
    with pytest.raises(ValidationError):
        StubMemberNsGroup(group_name="")


def test_stubmembernsgroup_serialize_stub_members():
    ns_group = StubMemberNsGroup(
        group_name="GroupName",
        stub_members=["server1.example.com", "server2.example.com"],
    )
    serialized_stub_members = ns_group.serialize_stub_members(ns_group.stub_members)
    assert serialized_stub_members == "server1.example.com,server2.example.com"


def test_stubmembernsgroup_serialize_stub_members_empty():
    ns_group = StubMemberNsGroup(group_name="GroupName", stub_members=[])
    serialized_stub_members = ns_group.serialize_stub_members(ns_group.stub_members)
    assert serialized_stub_members is None


def test_stubmembernsgroup_add_property_valid():
    ns_group = StubMemberNsGroup(group_name="GroupName")
    ns_group.add_property("EA-TestProperty", "TestValue")
    assert getattr(ns_group, "EA-TestProperty") == "TestValue"


def test_stubmembernsgroup_add_property_invalid():
    ns_group = StubMemberNsGroup(group_name="GroupName")
    with pytest.raises(Exception, match="Invalid field name: InvalidField"):
        ns_group.add_property("InvalidField", "TestValue")
