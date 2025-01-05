import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import StubZone
from src.ibx_sdk.nios.csv.enums import ZoneFormatTypeEnum


def test_stubzone_default_values():
    stub_zone = StubZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    assert stub_zone.stubzone == "stubzone"
    assert stub_zone.import_action is None
    assert stub_zone.fqdn == "example.com"
    assert stub_zone.view is None
    assert stub_zone.zone_format == ZoneFormatTypeEnum.FORWARD
    assert stub_zone.prefix is None
    assert stub_zone.disabled is None
    assert stub_zone.comment is None
    assert stub_zone.disable_forwarding is None
    assert stub_zone.stub_from is None
    assert stub_zone.stub_members is None
    assert stub_zone.ns_group is None
    assert stub_zone.ns_group_external is None


def test_stubzone_invalid_fqdn():
    with pytest.raises(ValidationError):
        StubZone(
            fqdn="",
            zone_format=ZoneFormatTypeEnum.FORWARD
        )


def test_stubzone_invalid_prefix():
    with pytest.raises(ValidationError):
        StubZone(
            fqdn="192.168.1.0",
            zone_format=ZoneFormatTypeEnum.IPV4,
            prefix=33
        )


def test_stubzone_serialize_stub_from():
    stub_zone = StubZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        stub_from=["server1.example.com/192.168.1.1"]
    )
    assert stub_zone.serialize_list_fields(stub_zone.stub_from) == "server1.example.com/192.168.1.1"


def test_stubzone_serialize_stub_members():
    stub_zone = StubZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        stub_members=["member1.example.com", "member2.example.com"]
    )
    assert stub_zone.serialize_list_fields(
        stub_zone.stub_members
    ) == "member1.example.com,member2.example.com"


def test_stubzone_add_property_valid():
    stub_zone = StubZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    stub_zone.add_property("EA-TestProperty", "TestValue")
    assert getattr(stub_zone, "EA-TestProperty") == "TestValue"


def test_stubzone_add_property_invalid():
    stub_zone = StubZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD
    )
    with pytest.raises(Exception, match="Invalid field name: TestProperty"):
        stub_zone.add_property("TestProperty", "TestValue")
