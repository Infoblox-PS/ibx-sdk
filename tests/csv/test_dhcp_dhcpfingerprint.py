import pytest
from src.ibx_sdk.nios.csv.dhcp import DhcpFingerprint
from src.ibx_sdk.nios.csv.enums import FingerprintTypeEnum, ProtocolTypeEnum


def test_dhcpfingerprint_default_values():
    dhcp_fingerprint = DhcpFingerprint(
        name="test_fingerprint",
        protocol=ProtocolTypeEnum.IPV4
    )
    assert dhcp_fingerprint.dhcpfingerprint == "dhcpfingerprint"
    assert dhcp_fingerprint.import_action is None
    assert dhcp_fingerprint.name == "test_fingerprint"
    assert dhcp_fingerprint.new_name is None
    assert dhcp_fingerprint.type == FingerprintTypeEnum.CUSTOM
    assert dhcp_fingerprint.comment is None
    assert dhcp_fingerprint.disable is None
    assert dhcp_fingerprint.vendor_id is None
    assert dhcp_fingerprint.option_sequence is None
    assert dhcp_fingerprint.device_class is None
    assert dhcp_fingerprint.protocol == ProtocolTypeEnum.IPV4


def test_dhcpfingerprint_custom_values():
    dhcp_fingerprint = DhcpFingerprint(
        name="custom_fingerprint",
        protocol=ProtocolTypeEnum.IPV6,
        comment="Custom DHCP Fingerprint",
        disable=True,
        vendor_id="Custom Vendor",
        option_sequence="1,2,3/ipv4",
        device_class="CustomClass",
        type=FingerprintTypeEnum.STANDARD
    )
    assert dhcp_fingerprint.dhcpfingerprint == "dhcpfingerprint"
    assert dhcp_fingerprint.import_action is None
    assert dhcp_fingerprint.name == "custom_fingerprint"
    assert dhcp_fingerprint.new_name is None
    assert dhcp_fingerprint.type == FingerprintTypeEnum.STANDARD
    assert dhcp_fingerprint.comment == "Custom DHCP Fingerprint"
    assert dhcp_fingerprint.disable is True
    assert dhcp_fingerprint.vendor_id == "Custom Vendor"
    assert dhcp_fingerprint.option_sequence == "1,2,3/ipv4"
    assert dhcp_fingerprint.device_class == "CustomClass"
    assert dhcp_fingerprint.protocol == ProtocolTypeEnum.IPV6


def test_dhcpfingerprint_invalid_add_property():
    dhcp_fingerprint = DhcpFingerprint(
        name="test_fingerprint",
        protocol=ProtocolTypeEnum.IPV4
    )
    with pytest.raises(Exception, match="Invalid field name: invalid-code"):
        dhcp_fingerprint.add_property("invalid-code", "value")


def test_dhcpfingerprint_valid_add_property():
    dhcp_fingerprint = DhcpFingerprint(
        name="test_fingerprint",
        protocol=ProtocolTypeEnum.IPV4
    )
    dhcp_fingerprint.add_property("EA-CustomField", "CustomValue")
    assert getattr(dhcp_fingerprint, "EA-CustomField") == "CustomValue"
