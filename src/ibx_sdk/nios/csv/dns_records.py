from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from .enums import ImportActionEnum, TargetRecordTypeEnum, HostAddressMatchEnum, IPv6AddressTypeEnum


class ARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    arecord: str = Field(alias="header-arecord", default="arecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    address: IPv4Address
    new_address: IPv4Address | None = Field(alias="_new_address", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None
    ddns_protected: bool | None = None
    ddns_principal: str | None = None
    creator: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class AAAARecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    aaaarecord: str = Field(alias="header-aaaarecord", default="aaaarecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    address: IPv6Address
    new_address: IPv6Address | None = Field(alias="_new_address", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None
    ddns_protected: bool | None = None
    ddns_principal: str | None = None
    creator: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class AliasRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    aliasrecord: str = Field(alias="header-aliasrecord", default="aliasrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    target_name: str
    new_target_name: str | None = Field(alias="_new_target_name", default=None)
    target_type: TargetRecordTypeEnum
    new_target_type: TargetRecordTypeEnum | None = Field(alias="_new_target_type", default=None)
    comment: str | None = None
    ttl: PositiveInt | None = None
    disabled: bool | None = None
    view: str | None = None
    creator: str | None = None


class DnameRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    dnamerecord: str = Field(alias="header-dnamerecord", default="dnamerecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    target: str
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class CnameRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    cnamerecord: str = Field(alias="header-cnamerecord", default="cnamerecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    canonical_name: str
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class MxRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    mxrecord: str = Field(alias="header-mxrecord", default="mxrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    mx: str
    new_mx: str | None = Field(alias="_new_mx", default=None)
    priority: int
    new_priority: int | None = Field(alias="_new_priority", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NaptrRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    naptrrecord: str = Field(alias="header-naptrrecord", default="naptrrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    order: PositiveInt
    new_order: PositiveInt | None = Field(alias="_new_order", default=None)
    preference: PositiveInt
    new_preference: PositiveInt | None = Field(alias="_new_preference", default=None)
    flags: str | None = None
    new_flags: str | None = Field(alias="_new_flags", default=None)
    services: str | None = None
    new_services: str | None = Field(alias="_new_service", default=None)
    regexp: str | None = None
    new_regexp: str | None = Field(alias="_new_regexp", default=None)
    replacement: str
    new_replacement: str | None = Field(alias="_new_replacement", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NsRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    nsrecord: str = Field(alias="header-nsrecord", default="nsrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    view: str | None = None
    dname: str
    new_dname: str | None = Field(alias="_new_dname", default=None)
    zone_nameservers: str  # list of ns_ip_address/auto_create_ptr, 192.168.10.53/True,...


class PtrRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    ptrrecord: str = Field(alias="header-ptrrecord", default="ptrrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    address: IPv4Address | IPv6Address
    new_address: IPv4Address | IPv6Address | None = Field(alias="_new_address", default=None)
    dname: str
    new_dname: str | None = Field(alias="_new_ptrdname", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class TxtRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    txtrecord: str = Field(alias="header-txtrecord", default="txtrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    text: str
    new_text: str | None = Field(alias="_new_text", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class SrvRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    srvrecord: str = Field(alias="header-srvrecord", default="srvrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    priority: int
    new_priority: int | None = Field(alias="_new_priority", default=None)
    weight: int
    new_weight: int | None = Field(alias="_new_weight", default=None)
    port: int
    new_port: int | None = Field(alias="_new_port", default=None)
    target: str
    new_target: str | None = Field(alias="_new_target", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class TlsaRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    tlsarecord: str = Field(alias="header-tlsarecord", default="tlsarecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    named: str
    certificate_usage: PositiveInt
    selector: PositiveInt
    matching_type: PositiveInt
    certificate_data: str
    new_certificate_data: str | None = Field(alias="_new_certificate_data", default=None)
    comment: str | None = None
    ttl: PositiveInt | None = None
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    disabled: bool | None = None
    creator: str | None = None


class CaaRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    caarecord: str = Field(alias="header-caarecord", default="caarecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    flag: PositiveInt
    type: str
    CA: str | None = None
    ca_details: str | None = None
    comment: str | None = None
    ttl: PositiveInt | None = None
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    disabled: bool | None = None
    view: str | None = None
    creator: str | None = None


class HostRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    hostrecord: str = Field(alias="header-hostrecord", default="hostrecord")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    new_fqdn: str | None = Field(alias="_new_fqdn", default=None)
    view: str | None = None
    network_view: str | None = None
    addresses: IPv4Address | None = None
    ipv6_addresses: IPv6Address | None = None
    aliases: str | None = None
    configure_for_dns: bool | None = None
    new_configure_for_dns: bool | None = Field(alias="_new_configure_for_dns", default=None)
    comment: str | None = None
    disabled: bool | None = None
    ttl: PositiveInt | None = None
    mac_address: str | None = None
    ddns_protected: bool | None = None
    configure_for_dhcp: bool | None = None
    deny_bootp: bool | None = None
    broadcast_address: IPv4Address | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    next_server: str | None = None
    lease_time: PositiveInt | None = None
    pxe_lease_time_enabled: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    routers: str | None = None
    match_option: str | None = None # MAC_ADDRESS/RESERVED
    ignore_dhcp_param_request_list: bool | None = None

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
    model_config = ConfigDict(extra="allow")

    hostaddress: str = Field(alias="header-hostaddress", default="hostaddress")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    view: str | None = None
    network_view: str | None = None
    address: IPv4Address
    new_address: IPv4Address | None = Field(alias="_new_address", default=None)
    mac_address: str | None = None
    configure_for_dhcp: bool | None = None
    configure_for_dns: bool | None = None
    deny_bootp: bool | None = None
    broadcast_address: IPv4Address | None = None
    option_logic_filters: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    next_server: str | None = None
    lease_time: PositiveInt | None = None
    pxe_lease_time_enabled: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    routers: str | None = None
    match_option: HostAddressMatchEnum | None = None
    ignore_dhcp_param_request_list: bool | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("OPTION-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class Ipv6HostAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6hostaddress: str = Field(alias="header-ipv6hostaddress", default="ipv6hostaddress")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    address_type: IPv6AddressTypeEnum | None = Field(default=IPv6AddressTypeEnum.ADDRESS)
    address: IPv6Address
    new_address: IPv6Address | None = Field(alias="_new_address", default=None)
    ipv6_prefix: PositiveInt | None = Field(ge=0, le=128, default=64)
    new_ipv6_prefix: PositiveInt | None = Field(alias="_new_ipv6_prefix", default=None)
    ipv6_prefix_bits: PositiveInt | None = Field(ge=0, le=128, default=64)
    configure_for_dhcp: bool | None = None
    configure_for_dns: bool | None = None
    match_option: str | None = Field(default='DUID')
    duid: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("OPTION-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")
