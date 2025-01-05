import pytest
from src.ibx_sdk.nios.csv.dhcp import OptionFilter
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_optionfilter_default_values():
    option_filter = OptionFilter(name="test_name")
    assert option_filter.optionfilter == "optionfilter"
    assert option_filter.import_action is None
    assert option_filter.name == "test_name"
    assert option_filter.new_name is None
    assert option_filter.comment is None
    assert option_filter.expression is None
    assert option_filter.boot_file is None
    assert option_filter.boot_server is None
    assert option_filter.lease_time is None
    assert option_filter.pxe_lease_time is None
    assert option_filter.next_server is None
    assert option_filter.option_space is None


def test_optionfilter_import_action():
    option_filter = OptionFilter(name="test_name", import_action=ImportActionEnum.INSERT)
    assert option_filter.import_action == ImportActionEnum.INSERT


def test_optionfilter_rename():
    option_filter = OptionFilter(name="test_name", new_name="new_test_name")
    assert option_filter.new_name == "new_test_name"


def test_optionfilter_comment():
    option_filter = OptionFilter(name="test_name", comment="This is a test comment.")
    assert option_filter.comment == "This is a test comment."


def test_optionfilter_expression():
    option_filter = OptionFilter(name="test_name", expression="option[123] == 5")
    assert option_filter.expression == "option[123] == 5"


def test_optionfilter_lease_time():
    option_filter = OptionFilter(name="test_name", lease_time=3600)
    assert option_filter.lease_time == 3600


def test_optionfilter_pxe_lease_time():
    option_filter = OptionFilter(name="test_name", pxe_lease_time=7200)
    assert option_filter.pxe_lease_time == 7200


def test_optionfilter_next_server():
    option_filter = OptionFilter(name="test_name", next_server="192.168.1.1")
    assert option_filter.next_server == "192.168.1.1"


def test_optionfilter_add_property_valid_code():
    option_filter = OptionFilter(name="test_name")
    option_filter.add_property("OPTION-test", "value")
    assert getattr(option_filter, "OPTION-test") == "value"


def test_optionfilter_add_property_invalid_code():
    option_filter = OptionFilter(name="test_name")
    with pytest.raises(Exception, match="Invalid field name: invalid-code"):
        option_filter.add_property("invalid-code", "value")
