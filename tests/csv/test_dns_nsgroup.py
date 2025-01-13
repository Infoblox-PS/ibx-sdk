import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import NsGroup
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_nsgroup_default_values():
    nsgroup = NsGroup(group_name="DefaultGroup")
    assert nsgroup.nsgroup == "nsgroup"
    assert nsgroup.group_name == "DefaultGroup"
    assert nsgroup.import_action is None
    assert nsgroup.new_group_name is None
    assert nsgroup.grid_primaries is None
    assert nsgroup.external_primaries is None
    assert nsgroup.external_secondaries is None
    assert nsgroup.grid_secondaries is None
    assert nsgroup.is_grid_default is None
    assert nsgroup.comment is None


def test_nsgroup_with_all_values():
    nsgroup = NsGroup(
        group_name="TestGroup",
        import_action=ImportActionEnum.INSERT_OVERRIDE,
        new_group_name="NewTestGroup",
        grid_primaries=["Primary1", "Primary2"],
        external_primaries=["ExtPrimary1"],
        external_secondaries=["ExtSecondary1"],
        grid_secondaries=["GridSecondary1"],
        is_grid_default=True,
        comment="Test comment"
    )
    assert nsgroup.group_name == "TestGroup"
    assert nsgroup.import_action == ImportActionEnum.INSERT_OVERRIDE
    assert nsgroup.new_group_name == "NewTestGroup"
    assert nsgroup.serialize_list_fields(nsgroup.grid_primaries) == "Primary1,Primary2"
    assert nsgroup.serialize_list_fields(nsgroup.external_primaries) == "ExtPrimary1"
    assert nsgroup.serialize_list_fields(nsgroup.external_secondaries) == "ExtSecondary1"
    assert nsgroup.serialize_list_fields(nsgroup.grid_secondaries) == "GridSecondary1"
    assert nsgroup.is_grid_default is True
    assert nsgroup.comment == "Test comment"


def test_nsgroup_invalid_group_name():
    with pytest.raises(ValidationError):
        NsGroup(group_name=None)


def test_nsgroup_add_valid_property():
    nsgroup = NsGroup(group_name="TestGroup")
    nsgroup.add_property("EA-TestProperty", "TestValue")
    assert getattr(nsgroup, "EA-TestProperty") == "TestValue"


def test_nsgroup_add_invalid_property():
    nsgroup = NsGroup(group_name="TestGroup")
    with pytest.raises(Exception, match="Invalid field name: InvalidProp"):
        nsgroup.add_property("InvalidProp", "TestValue")


def test_nsgroup_list_to_csv_conversion():
    assert NsGroup.list_to_csv([]) is None
    assert NsGroup.list_to_csv(["item1", "item2"]) == "item1,item2"
    assert NsGroup.list_to_csv(None) is None
