# File: tests/test_dns.py

import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import AuthZone
from src.ibx_sdk.nios.csv.enums import ZoneFormatTypeEnum


def test_authzone_default_values():
    auth_zone = AuthZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )

    assert auth_zone.authzone == "authzone"
    assert auth_zone.fqdn == "example.com"
    assert auth_zone.zone_format == ZoneFormatTypeEnum.FORWARD
    assert auth_zone.import_action is None
    assert auth_zone.view is None
    assert auth_zone.prefix is None
    assert auth_zone.new_prefix is None
    assert auth_zone.is_multimaster is None
    assert auth_zone.grid_primaries is None
    assert auth_zone.external_primaries is None
    assert auth_zone.grid_secondaries is None
    assert auth_zone.external_secondaries is None
    assert auth_zone.ns_group is None
    assert auth_zone.comment is None
    assert auth_zone.disabled is None
    assert auth_zone.create_underscore_zones is None
    assert auth_zone.allow_active_dir is None
    assert auth_zone.soa_refresh is None
    assert auth_zone.soa_retry is None
    assert auth_zone.soa_expire is None
    assert auth_zone.soa_default_ttl is None
    assert auth_zone.soa_negative_ttl is None
    assert auth_zone.soa_mnames is None
    assert auth_zone.soa_email is None
    assert auth_zone.soa_serial_number is None
    assert auth_zone.disable_forwarding is None
    assert auth_zone.allow_update_forwarding is None
    assert auth_zone.update_forwarding is None
    assert auth_zone.allow_transfer is None
    assert auth_zone.allow_update is None
    assert auth_zone.allow_query is None
    assert auth_zone.notify_delay is None


def test_authzone_required_fields():
    with pytest.raises(ValidationError):
        AuthZone(
            zone_format=ZoneFormatTypeEnum.FORWARD
        )

    with pytest.raises(ValidationError):
        AuthZone(
            fqdn="example.com"
        )


def test_authzone_invalid_fields():
    with pytest.raises(Exception, match="Invalid field name: INVALID-EA-FIELD"):
        auth_zone = AuthZone(
            fqdn="example.com",
            zone_format=ZoneFormatTypeEnum.FORWARD
        )
        auth_zone.add_property("INVALID-EA-FIELD", "some_value")


def test_authzone_list_to_csv():
    items = ["item1", "item2", "item3"]
    csv_result = AuthZone.list_to_csv(items)
    assert csv_result == "item1,item2,item3"

    empty_result = AuthZone.list_to_csv([])
    assert empty_result is None

    none_result = AuthZone.list_to_csv(None)
    assert none_result is None


def test_authzone_serialization():
    auth_zone = AuthZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        grid_primaries=["192.168.1.1", "192.168.1.2"],
    )
    serialized_value = auth_zone.serialize_list_fields(auth_zone.grid_primaries)
    assert serialized_value == "192.168.1.1,192.168.1.2"
