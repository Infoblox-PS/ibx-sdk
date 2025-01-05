from datetime import datetime

import pytest
from src.ibx_sdk.nios.csv.dhcp import MacFilterAddress
from src.ibx_sdk.nios.csv.enums import ImportActionEnum


def test_macfilteraddress_default_values():
    mac_filter = MacFilterAddress(
        parent="Filter1",
        mac_address="00:1A:2B:3C:4D:5E"
    )
    assert mac_filter.macfilteraddress == "macfilteraddress"
    assert mac_filter.import_action is None
    assert mac_filter.parent == "Filter1"
    assert mac_filter.mac_address == "00:1A:2B:3C:4D:5E"
    assert mac_filter.new_mac_address is None
    assert mac_filter.is_registered_user is None
    assert mac_filter.registered_user is None
    assert mac_filter.comment is None


def test_macfilteraddress_custom_values():
    expire_time = datetime(2024, 1, 1, 12, 0, 0)
    mac_filter = MacFilterAddress(
        parent="Filter1",
        mac_address="00:1A:2B:3C:4D:5E",
        new_mac_address="00:1A:2B:3C:4D:5F",
        is_registered_user=True,
        registered_user="RegisteredUser",
        guest_email="guest@example.com",
        guest_phone="123456789",
        never_expires=False,
        expire_time=expire_time,
        comment="This is a test comment"
    )
    assert mac_filter.macfilteraddress == "macfilteraddress"
    assert mac_filter.parent == "Filter1"
    assert mac_filter.mac_address == "00:1A:2B:3C:4D:5E"
    assert mac_filter.new_mac_address == "00:1A:2B:3C:4D:5F"
    assert mac_filter.is_registered_user is True
    assert mac_filter.registered_user == "RegisteredUser"
    assert mac_filter.guest_email == "guest@example.com"
    assert mac_filter.guest_phone == "123456789"
    assert mac_filter.never_expires is False
    assert mac_filter.expire_time == expire_time
    assert mac_filter.comment == "This is a test comment"


def test_macfilteraddress_invalid_add_property():
    mac_filter = MacFilterAddress(
        parent="Filter1",
        mac_address="00:1A:2B:3C:4D:5E"
    )
    with pytest.raises(Exception) as exc_info:
        mac_filter.add_property("INVALID-CODE", "value")
    assert "Invalid field name" in str(exc_info.value)


def test_macfilteraddress_valid_add_property():
    mac_filter = MacFilterAddress(
        parent="Filter1",
        mac_address="00:1A:2B:3C:4D:5E"
    )
    mac_filter.add_property("EA-Test", "value")
    assert getattr(mac_filter, "EA-Test") == "value"
    mac_filter.add_property("ADMGRP-Test", "value")
    assert getattr(mac_filter, "ADMGRP-Test") == "value"
