import pytest
from pydantic import ValidationError
from src.ibx_sdk.nios.csv.dns import DelegatedZone
from src.ibx_sdk.nios.csv.enums import ZoneFormatTypeEnum, ImportActionEnum


def test_delegatedzone_default_values():
    delegated_zone = DelegatedZone(
        fqdn="example.com", zone_format=ZoneFormatTypeEnum.FORWARD
    )
    assert delegated_zone.delegatedzone == "delegatedzone"
    assert delegated_zone.fqdn == "example.com"
    assert delegated_zone.zone_format == ZoneFormatTypeEnum.FORWARD
    assert delegated_zone.view is None
    assert delegated_zone.prefix is None
    assert delegated_zone.disabled is None
    assert delegated_zone.comment is None
    assert delegated_zone.delegate_to is None
    assert delegated_zone.delegated_ttl is None
    assert delegated_zone.ns_group is None
    assert delegated_zone.new_prefix is None
    assert delegated_zone.ddns_protected is None
    assert delegated_zone.ddns_principal is None
    assert delegated_zone.import_action is None


def test_delegatedzone_with_all_fields():
    delegated_zone = DelegatedZone(
        fqdn="sub.example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        view="view_name",
        prefix=24,
        disabled=True,
        comment="This is a comment",
        delegate_to=["ns1.example.com", "ns2.example.com"],
        delegated_ttl=3600,
        ns_group="ns_group_name",
        new_prefix=25,
        ddns_protected=False,
        ddns_principal="principal",
        import_action=ImportActionEnum.INSERT_OVERRIDE,
    )
    assert delegated_zone.fqdn == "sub.example.com"
    assert delegated_zone.zone_format == ZoneFormatTypeEnum.FORWARD
    assert delegated_zone.view == "view_name"
    assert delegated_zone.prefix == 24
    assert delegated_zone.disabled is True
    assert delegated_zone.comment == "This is a comment"
    assert delegated_zone.delegate_to == ["ns1.example.com", "ns2.example.com"]
    assert delegated_zone.delegated_ttl == 3600
    assert delegated_zone.ns_group == "ns_group_name"
    assert delegated_zone.new_prefix == 25
    assert delegated_zone.ddns_protected is False
    assert delegated_zone.ddns_principal == "principal"
    assert delegated_zone.import_action == ImportActionEnum.INSERT_OVERRIDE


def test_delegatedzone_invalid_field():
    delegated_zone = DelegatedZone(
        fqdn="example.com", zone_format=ZoneFormatTypeEnum.FORWARD
    )
    with pytest.raises(Exception) as excinfo:
        delegated_zone.add_property("invalid-field", "value")
    assert "Invalid field name: invalid-field" in str(excinfo.value)


def test_delegatedzone_extra_field():
    delegated_zone = DelegatedZone(
        fqdn="example.com", zone_format=ZoneFormatTypeEnum.FORWARD
    )
    delegated_zone.add_property("EA-Custom", "custom_value")
    assert getattr(delegated_zone, "EA-Custom") == "custom_value"


def test_delegatedzone_invalid_prefix():
    with pytest.raises(ValidationError):
        DelegatedZone(
            fqdn="example.com", zone_format=ZoneFormatTypeEnum.FORWARD, prefix=-5
        )


def test_delegatedzone_serialize_delegate_to():
    delegated_zone = DelegatedZone(
        fqdn="example.com",
        zone_format=ZoneFormatTypeEnum.FORWARD,
        delegate_to=["ns1.example.com", "ns2.example.com"],
    )
    assert (
        delegated_zone.serialize_delegate_to(delegated_zone.delegate_to)
        == "ns1.example.com,ns2.example.com"
    )
    assert delegated_zone.serialize_delegate_to(None) is None
