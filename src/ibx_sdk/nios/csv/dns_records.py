from ipaddress import IPv4Address, IPv6Address
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, PositiveInt, IPvAnyAddress

from .enums import (
    CreatorEnum,
    ImportActionEnum,
    TargetRecordTypeEnum,
    HostAddressMatchEnum,
    IPv6AddressTypeEnum,
)


class ARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    arecord: str = Field(alias="header-arecord", default="arecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    address: IPv4Address
    new_address: Optional[IPv4Address] = Field(
        alias="_new_address", default=None
    )
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class AAAARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    aaaarecord: str = Field(alias="header-aaaarecord", default="aaaarecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    address: IPv6Address
    new_address: Optional[IPv6Address] = Field(
        alias="_new_address", default=None
    )
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class AliasRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    aliasrecord: str = Field(alias="header-aliasrecord", default="aliasrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    target_name: str
    new_target_name: Optional[str] = Field(
        alias="_new_target_name", default=None
    )
    target_type: TargetRecordTypeEnum
    new_target_type: Optional[TargetRecordTypeEnum] = Field(
        alias="_new_target_type", default=None
    )
    comment: Optional[str] = None
    ttl: Optional[PositiveInt] = None
    disabled: Optional[bool] = None
    view: Optional[str] = None
    creator: Optional[CreatorEnum] = None


class DNAMERecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    dnamerecord: str = Field(alias="header-dnamerecord", default="dnamerecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    target: str
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class CNAMERecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    cnamerecord: str = Field(alias="header-cnamerecord", default="cnamerecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    canonical_name: str
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class MXRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    mxrecord: str = Field(alias="header-mxrecord", default="mxrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    mx: str
    new_mx: Optional[str] = Field(alias="_new_mx", default=None)
    priority: int
    new_priority: Optional[int] = Field(alias="_new_priority", default=None)
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NAPTRRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    naptrrecord: str = Field(alias="header-naptrrecord", default="naptrrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    order: PositiveInt
    new_order: Optional[PositiveInt] = Field(alias="_new_order", default=None)
    preference: PositiveInt
    new_preference: Optional[PositiveInt] = Field(
        alias="_new_preference", default=None
    )
    flags: Optional[str] = None
    new_flags: Optional[str] = Field(alias="_new_flags", default=None)
    services: Optional[str] = None
    new_services: Optional[str] = Field(alias="_new_service", default=None)
    regexp: Optional[str] = None
    new_regexp: Optional[str] = Field(alias="_new_regexp", default=None)
    replacement: str
    new_replacement: Optional[str] = Field(
        alias="_new_replacement", default=None
    )
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NSRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    nsrecord: str = Field(alias="header-nsrecord", default="nsrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    view: Optional[str] = None
    dname: str
    new_dname: Optional[str] = Field(alias="_new_dname", default=None)
    zone_nameservers: (
        str  # list of ns_ip_address/auto_create_ptr, 192.168.10.53/True,...
    )


class PTRRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    ptrrecord: str = Field(alias="header-ptrrecord", default="ptrrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    address: Optional[IPvAnyAddress] = Field(default=None)
    new_address: Optional[str] = Field(alias="_new_address", default=None)
    dname: str
    new_dname: Optional[str] = Field(alias="_new_ptrdname", default=None)
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class TXTRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    txtrecord: str = Field(alias="header-txtrecord", default="txtrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    text: str
    new_text: Optional[str] = Field(alias="_new_text", default=None)
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class SRVRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    srvrecord: str = Field(alias="header-srvrecord", default="srvrecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    priority: int
    new_priority: Optional[int] = Field(alias="_new_priority", default=None)
    weight: int
    new_weight: Optional[int] = Field(alias="_new_weight", default=None)
    port: int
    new_port: Optional[int] = Field(alias="_new_port", default=None)
    target: str
    new_target: Optional[str] = Field(alias="_new_target", default=None)
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    ddns_protected: Optional[bool] = None
    ddns_principal: Optional[str] = None
    creator: Optional[CreatorEnum] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class TLSARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    tlsarecord: str = Field(alias="header-tlsarecord", default="tlsarecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    named: str
    certificate_usage: PositiveInt
    selector: PositiveInt
    matching_type: PositiveInt
    certificate_data: str
    new_certificate_data: Optional[str] = Field(
        alias="_new_certificate_data", default=None
    )
    comment: Optional[str] = None
    ttl: Optional[PositiveInt] = None
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    disabled: Optional[bool] = None
    creator: Optional[CreatorEnum] = None


class CAARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    caarecord: str = Field(alias="header-caarecord", default="caarecord")
    import_action: Optional[ImportActionEnum] = Field(
        alias="import-action", default=None
    )
    flag: PositiveInt
    type: str
    ca: Optional[str] = None
    ca_details: Optional[str] = None
    comment: Optional[str] = None
    ttl: Optional[PositiveInt] = None
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    disabled: Optional[bool] = None
    view: Optional[str] = None
    creator: Optional[CreatorEnum] = None


class HostRecord(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    hostrecord: str = Field(alias="header-hostrecord", default="hostrecord")
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    fqdn: str
    new_fqdn: Optional[str] = Field(alias="_new_fqdn", default=None)
    view: Optional[str] = None
    network_view: Optional[str] = None
    addresses: Optional[IPv4Address] = None
    ipv6_addresses: Optional[IPv6Address] = None
    aliases: Optional[str] = None
    configure_for_dns: Optional[bool] = None
    new_configure_for_dns: Optional[bool] = Field(
        alias="_new_configure_for_dns", default=None
    )
    comment: Optional[str] = None
    disabled: Optional[bool] = None
    ttl: Optional[PositiveInt] = None
    mac_address: Optional[str] = None
    ddns_protected: Optional[bool] = None
    configure_for_dhcp: Optional[bool] = None
    deny_bootp: Optional[bool] = None
    broadcast_address: Optional[IPv4Address] = None
    boot_file: Optional[str] = None
    boot_server: Optional[str] = None
    next_server: Optional[str] = None
    lease_time: Optional[PositiveInt] = None
    pxe_lease_time_enabled: Optional[bool] = None
    pxe_lease_time: Optional[PositiveInt] = None
    domain_name: Optional[str] = None
    domain_name_servers: Optional[str] = None
    routers: Optional[str] = None
    match_option: Optional[str] = None  # MAC_ADDRESS/RESERVED
    ignore_dhcp_param_request_list: Optional[bool] = None

    def add_property(self, code: str, value: str):
        if (
            code.startswith("OPTION-")
            or code.startswith("EA-")
            or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class HostAddress(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    hostaddress: str = Field(
        serialization_alias="header-hostaddress", default="hostaddress"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    parent: str
    view: Optional[str] = None
    network_view: Optional[str] = None
    address: IPv4Address
    new_address: Optional[IPv4Address] = Field(
        alias="_new_address", default=None
    )
    mac_address: Optional[str] = None
    configure_for_dhcp: Optional[bool] = None
    configure_for_dns: Optional[bool] = None
    deny_bootp: Optional[bool] = None
    broadcast_address: Optional[IPv4Address] = None
    option_logic_filters: Optional[str] = None
    boot_file: Optional[str] = None
    boot_server: Optional[str] = None
    next_server: Optional[str] = None
    lease_time: Optional[PositiveInt] = None
    pxe_lease_time_enabled: Optional[bool] = None
    pxe_lease_time: Optional[PositiveInt] = None
    domain_name: Optional[str] = None
    domain_name_servers: Optional[str] = None
    routers: Optional[str] = None
    match_option: Optional[HostAddressMatchEnum] = None
    ignore_dhcp_param_request_list: Optional[bool] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("OPTION-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class Ipv6HostAddress(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    ipv6hostaddress: str = Field(
        serialization_alias="header-ipv6hostaddress", default="ipv6hostaddress"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    view: Optional[str] = None
    network_view: Optional[str] = None
    parent: str
    address_type: Optional[IPv6AddressTypeEnum] = Field(
        default=IPv6AddressTypeEnum.ADDRESS
    )
    address: IPv6Address
    new_address: Optional[IPv6Address] = Field(
        alias="_new_address", default=None
    )
    ipv6_prefix: Optional[PositiveInt] = Field(ge=0, le=128, default=None)
    new_ipv6_prefix: Optional[PositiveInt] = Field(
        alias="_new_ipv6_prefix", default=None
    )
    ipv6_prefix_bits: Optional[PositiveInt] = Field(ge=0, le=128, default=None)
    configure_for_dhcp: Optional[bool] = None
    configure_for_dns: Optional[bool] = None
    match_option: Optional[str] = None
    duid: Optional[str] = None
    domain_name: Optional[str] = None
    domain_name_servers: Optional[str] = None
    valid_lifetime: Optional[PositiveInt] = None
    preferred_lifetime: Optional[PositiveInt] = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("OPTION-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")
