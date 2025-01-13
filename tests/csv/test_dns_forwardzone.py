import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import ForwardZone
from src.ibx_sdk.nios.csv.enums import ZoneFormatTypeEnum, ImportActionEnum


def test_forwardzone_default_values():
    forward_zone = ForwardZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    assert forward_zone.forwardzone == "forwardzone"
    assert forward_zone.fqdn == "example.com"
    assert forward_zone.zone_format == ZoneFormatTypeEnum.FORWARD
    assert forward_zone.import_action is None
    assert forward_zone.view is None
    assert forward_zone.prefix is None
    assert forward_zone.disabled is None
    assert forward_zone.comment is None
    assert forward_zone.forward_to is None
    assert forward_zone.forwarding_servers is None
    assert forward_zone.forwarders_only is True
    assert forward_zone.ns_group is None
    assert forward_zone.ns_group_external is None
    assert forward_zone.disable_ns_generation is True


def test_forwardzone_with_optional_values():
    forward_zone = ForwardZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        view="default",
        prefix="192.168",
        disabled=True,
        comment="Test comment",
        forward_to=["forwarder1.com", "forwarder2.com"],
        forwarding_servers=["server1.com"],
        forwarders_only=False,
        ns_group="group1",
        ns_group_external="external_group",
        disable_ns_generation=False,
        import_action=ImportActionEnum.INSERT
    )
    assert forward_zone.view == "default"
    assert forward_zone.prefix == "192.168"
    assert forward_zone.disabled is True
    assert forward_zone.comment == "Test comment"
    assert forward_zone.forward_to == ["forwarder1.com", "forwarder2.com"]
    assert forward_zone.forwarding_servers == ["server1.com"]
    assert forward_zone.forwarders_only is False
    assert forward_zone.ns_group == "group1"
    assert forward_zone.ns_group_external == "external_group"
    assert forward_zone.disable_ns_generation is False
    assert forward_zone.import_action == ImportActionEnum.INSERT


def test_forwardzone_invalid_fqdn():
    with pytest.raises(ValidationError):
        ForwardZone(
            fqdn="",
            zone_format=ZoneFormatTypeEnum.FORWARD
        )


def test_forwardzone_serialize_list_fields():
    forward_zone = ForwardZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        forward_to=["forwarder1.com", "forwarder2.com"],
        forwarding_servers=["server1.com", "server2.com"]
    )
    assert forward_zone.serialize_list_fields(
        forward_zone.forward_to) == "forwarder1.com,forwarder2.com"
    assert forward_zone.serialize_list_fields(
        forward_zone.forwarding_servers) == "server1.com,server2.com"


def test_forwardzone_add_valid_property():
    forward_zone = ForwardZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    forward_zone.add_property("EA-test", "value")
    assert getattr(forward_zone, "EA-test") == "value"


def test_forwardzone_add_invalid_property():
    forward_zone = ForwardZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    with pytest.raises(Exception, match="Invalid field name: invalid_property"):
        forward_zone.add_property("invalid_property", "value")
