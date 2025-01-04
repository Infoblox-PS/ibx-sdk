import pytest

from src.ibx_sdk.nios.csv.dhcp import NetworkView
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_networkview_default_values():
    network_view = NetworkView(name="test_name")
    assert network_view.networkview == "networkview"
    assert network_view.import_action is None
    assert network_view.name == "test_name"
    assert network_view.new_name is None
    assert network_view.comment is None


def test_networkview_custom_import_action():
    network_view = NetworkView(name="test_name", import_action=ImportActionEnum.OVERRIDE)
    assert network_view.import_action == ImportActionEnum.OVERRIDE


def test_networkview_add_property_valid_code():
    network_view = NetworkView(name="test_name")
    network_view.add_property("EA-example", "example_value")
    assert getattr(network_view, "EA-example") == "example_value"


def test_networkview_add_property_admin_group():
    network_view = NetworkView(name="test_name")
    network_view.add_property("ADMGRP-myadmin", "myadmin value")
    assert getattr(network_view, "ADMGRP-myadmin") == "myadmin value"


def test_networkview_add_property_invalid_code():
    network_view = NetworkView(name="test_name")
    with pytest.raises(Exception) as excinfo:
        network_view.add_property("INVALID-code", "value")
    assert "Invalid field name" in str(excinfo.value)
