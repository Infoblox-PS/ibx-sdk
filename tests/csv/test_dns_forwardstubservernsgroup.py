import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import ForwardStubServerNsGroup
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_forwardstubservernsgroup_default_values():
    ns_group = ForwardStubServerNsGroup(
        group_name="DefaultStubGroup"
    )
    assert ns_group.forwardstubservernsgroup == "forwardstubservernsgroup"
    assert ns_group.group_name == "DefaultStubGroup"
    assert ns_group.import_action is None
    assert ns_group.new_group_name is None
    assert ns_group.comment is None
    assert ns_group.external_servers is None


def test_forwardstubservernsgroup_with_all_fields():
    ns_group = ForwardStubServerNsGroup(
        group_name="StubGroup",
        new_group_name="NewStubGroup",
        comment="Test comment",
        external_servers=["192.168.0.1", "example.com"],
        import_action=ImportActionEnum.OVERRIDE
    )
    assert ns_group.forwardstubservernsgroup == "forwardstubservernsgroup"
    assert ns_group.group_name == "StubGroup"
    assert ns_group.new_group_name == "NewStubGroup"
    assert ns_group.comment == "Test comment"
    assert ns_group.external_servers == ["192.168.0.1", "example.com"]
    assert ns_group.import_action == ImportActionEnum.OVERRIDE


def test_forwardstubservernsgroup_external_servers_serialization():
    ns_group = ForwardStubServerNsGroup(
        group_name="SerializedGroup",
        external_servers=["192.168.1.1", "dns.example.com"]
    )
    serialized_servers = ns_group.serialize_external_servers(ns_group.external_servers)
    assert serialized_servers == "192.168.1.1,dns.example.com"


def test_forwardstubservernsgroup_external_servers_none_serialization():
    ns_group = ForwardStubServerNsGroup(group_name="NoServersGroup")
    serialized_servers = ns_group.serialize_external_servers(ns_group.external_servers)
    assert serialized_servers is None


def test_forwardstubservernsgroup_add_property_valid():
    ns_group = ForwardStubServerNsGroup(group_name="PropertyGroup")
    ns_group.add_property("EA-custom_property", "custom_value")
    assert getattr(ns_group, "EA-custom_property") == "custom_value"


def test_forwardstubservernsgroup_add_property_invalid():
    ns_group = ForwardStubServerNsGroup(group_name="InvalidPropertyGroup")
    with pytest.raises(Exception, match="Invalid field name: invalid_property"):
        ns_group.add_property("invalid_property", "value")


def test_forwardstubservernsgroup_missing_required_fields():
    with pytest.raises(ValidationError):
        ForwardStubServerNsGroup()
