import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dhcp import DhcpMacFilter
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_dhcpmacfilter_default_values():
    dhcpmacfilter = DhcpMacFilter(name="TestFilter")
    assert dhcpmacfilter.dhcpmacfilter == "dhcpmacfilter"
    assert dhcpmacfilter.import_action is None
    assert dhcpmacfilter.name == "TestFilter"
    assert dhcpmacfilter.new_name is None
    assert dhcpmacfilter.never_expires is None
    assert dhcpmacfilter.expiration_interval is None
    assert dhcpmacfilter.enforce_expiration_time is None
    assert dhcpmacfilter.comment is None


def test_dhcpmacfilter_custom_values():
    dhcpmacfilter = DhcpMacFilter(
        name="CustomFilter",
        import_action=ImportActionEnum.INSERT,
        new_name="NewFilterName",
        never_expires=True,
        expiration_interval=3600,
        enforce_expiration_time=True,
        comment="This is a custom comment.",
    )
    assert dhcpmacfilter.name == "CustomFilter"
    assert dhcpmacfilter.import_action == ImportActionEnum.INSERT
    assert dhcpmacfilter.new_name == "NewFilterName"
    assert dhcpmacfilter.never_expires is True
    assert dhcpmacfilter.expiration_interval == 3600
    assert dhcpmacfilter.enforce_expiration_time is True
    assert dhcpmacfilter.comment == "This is a custom comment."


def test_dhcpmacfilter_add_valid_property():
    dhcpmacfilter = DhcpMacFilter(name="ValidPropertyTest")
    dhcpmacfilter.add_property("EA-TestProperty", "TestValue")
    assert getattr(dhcpmacfilter, "EA-TestProperty") == "TestValue"


def test_dhcpmacfilter_add_invalid_property():
    dhcpmacfilter = DhcpMacFilter(name="InvalidPropertyTest")
    with pytest.raises(Exception, match="Invalid field name: INVALID-CODE"):
        dhcpmacfilter.add_property("INVALID-CODE", "TestValue")


def test_dhcpmacfilter_missing_required_field():
    with pytest.raises(ValidationError) as exc_info:
        DhcpMacFilter()
    assert "Field required" in str(exc_info.value)
    assert "name" in str(exc_info.value)
