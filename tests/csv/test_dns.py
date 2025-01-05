import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import DelegationNsGroup
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_delegationnsgroup_default_values():
    delegation_ns_group = DelegationNsGroup(
        group_name="example_ns_group"
    )
    assert delegation_ns_group.delegationnsgroup == "delegationnsgroup"
    assert delegation_ns_group.group_name == "example_ns_group"
    assert delegation_ns_group.import_action is None
    assert delegation_ns_group.new_group_name is None
    assert delegation_ns_group.delegate_to is None
    assert delegation_ns_group.comment is None


def test_delegationnsgroup_with_values():
    delegation_ns_group = DelegationNsGroup(
        group_name="test_group",
        new_group_name="new_test_group",
        delegate_to=["server1.example.com", "192.168.0.1"],
        comment="This is a test comment",
        import_action=ImportActionEnum.OVERRIDE
    )
    assert delegation_ns_group.group_name == "test_group"
    assert delegation_ns_group.new_group_name == "new_test_group"
    assert delegation_ns_group.delegate_to == ["server1.example.com", "192.168.0.1"]
    assert delegation_ns_group.comment == "This is a test comment"
    assert delegation_ns_group.import_action == ImportActionEnum.OVERRIDE


def test_delegationnsgroup_delegate_to_serialization():
    delegation_ns_group = DelegationNsGroup(
        group_name="test_group",
        delegate_to=["server1.example.com", "192.168.0.1"]
    )
    serialized_delegate_to = delegation_ns_group.model_dump()["delegate_to"]
    assert serialized_delegate_to == "server1.example.com,192.168.0.1"


def test_delegationnsgroup_invalid_group_name():
    with pytest.raises(ValidationError):
        DelegationNsGroup(
            group_name=None  # group_name is a required field
        )


def test_delegationnsgroup_invalid_delegate_to():
    with pytest.raises(ValidationError):
        DelegationNsGroup(
            group_name="test_group",
            delegate_to=123  # delegate_to must be a list of strings
        )


def test_delegationnsgroup_invalid_import_action():
    with pytest.raises(ValidationError):
        DelegationNsGroup(
            group_name="test_group",
            import_action="INVALID_ACTION"  # Must be a valid ImportActionEnum
        )
