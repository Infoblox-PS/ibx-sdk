import re
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator, PositiveInt
from typing_extensions import Self

from .enums import (
    ImportActionEnum,
    LeasePerClientSettingsEnum,
    ServerAssociationTypeEnum,
    IPv6AddressTypeEnum,
    MatchOptionEnum,
    FingerprintTypeEnum,
    ProtocolTypeEnum,
    DhcpTypeEnum,
    FailoverServerType
)


class GridDhcp(BaseModel):
    model_config = ConfigDict(extra="allow")

    griddhcp: str = Field(
        "griddhcp",
        frozen=True,
        alias="header-griddhcp",
        description="Default header for griddhcp"
    )
    authority: bool | None = None
    domain_name: str | None = None
    recycle_leases: bool | None = None
    ignore_dhcp_option_list_request: bool | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    bootfile: str | None = None
    bootserver: str | None = None
    nextserver: str | None = None
    deny_bootp: bool | None = None
    enable_ddns: bool | None = None
    ddns_use_option81: bool | None = None
    ddns_server_always_updates: bool | None = None
    ddns_generate_hostname: bool | None = None
    ddns_ttl: PositiveInt | None = None
    retry_ddns_updates: bool | None = None
    ddns_retry_interval: PositiveInt | None = None  # you must set retry_ddns_updates to True to modify this
    enable_dhcp_thresholds: bool | None = None
    high_water_mark: PositiveInt | None = None
    high_water_mark_reset: PositiveInt | None = None
    low_water_mark: PositiveInt | None = None
    low_water_mark_reset: PositiveInt | None = None
    enable_email_warnings: bool | None = None
    enable_snmp_warnings: bool | None = None
    email_list: str | None = None
    ipv6_domain_name_servers: str | None = None
    ping_count: PositiveInt | None = None
    ping_timeout: PositiveInt | None = None
    capture_hostname: bool | None = None
    enable_leasequery: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    ipv6_update_dns_on_lease_renewal: bool | None = None
    txt_record_handling: str | None = None
    lease_scavenge_time: PositiveInt | None = None
    failover_port: PositiveInt | None = None
    enable_fingerprint: bool | None = None
    ipv6_enable_ddns: bool | None = None
    ipv6_enable_option_fqdn: bool | None = None
    ipv6_ddns_server_always_updates: bool | None = None
    ipv6_generate_hostname: bool | None = None
    ipv6_ddns_domainname: str | None = None
    ipv6_ddns_ttl: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    valid_lifetime: PositiveInt | None = None
    ipv6_domain_name: str | None = None
    ipv6_txt_record_handling: str | None = None
    ipv6_capture_hostname: bool | None = None
    ipv6_recycle_leases: bool | None = None
    ipv6_enable_retry_updates: bool | None = None
    ipv6_retry_updates_interval: PositiveInt | None = None
    ddns_domainname: str | None = None
    leases_per_client_settings: LeasePerClientSettingsEnum | None = None
    ignore_client_identifier: bool | None = None
    disable_all_nac_filters: bool | None = None
    format_log_option_82: str | None = None
    v6_leases_scavenging_enabled: bool | None = None
    v6_leases_scavenging_grace_period: PositiveInt | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class MemberDhcp(BaseModel):
    model_config = ConfigDict(extra="allow")

    memberdhcp: str = Field(
        "memberdhcp",
        frozen=True,
        alias="header-memberdhcp",
        description="Default header for memberdhcp",
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    broadcast_address: IPv4Address | None
    domain_name_servers: str | None
    ignore_client_requested_options: bool | None
    pxe_lease_time: PositiveInt | None
    lease_time: PositiveInt | None
    domain_name: str | None
    routers: str | None
    option_logic_filters: str | None
    enable_pxe_lease_time: bool | None
    deny_bootp: bool | None
    bootfile: str | None
    bootserver: str | None
    nextserver: str | None
    enable_thresholds: bool | None
    range_high_water_mark: PositiveInt | None
    range_high_water_mark_reset: PositiveInt | None
    range_low_water_mark: PositiveInt | None
    range_low_water_mark_reset: PositiveInt | None
    enable_threshold_email_warnings: bool | None
    enable_threshold_snmp_warnings: bool | None
    threshold_email_addresses: str | None
    enable_ddns: bool | None
    ddns_use_option81: bool | None
    always_update_dns: bool | None
    generate_hostname: bool | None
    update_static_leases: bool | None
    ddns_ttl: PositiveInt | None
    update_dns_on_lease_renewal: bool | None
    preferred_lifetime: PositiveInt | None
    valid_lifetime: PositiveInt | None
    name: str
    is_authoritative: bool | None
    recycle_leases: bool | None
    ping_count: PositiveInt | None
    ping_timeout: PositiveInt | None
    enable_leasequery: bool | None
    retry_ddns_updates: bool | None
    ddns_retry_interval: PositiveInt | None  # you must set retry_ddns_updates to True to modify this
    lease_scavenge_time: PositiveInt | None
    enable_fingerprint: bool | None
    ipv6_enable_ddns: bool | None
    ipv6_ddns_enable_option_fqdn: bool | None
    ipv6_generate_hostname: bool | None
    ipv6_ddns_domainname: str | None
    ipv6_ddns_ttl: PositiveInt | None
    ipv6_domain_name_servers: str | None
    ipv6_domain_name: str | None
    ipv6_recycle_leases: bool | None
    ipv6_server_duid: str | None
    ipv6_enable_retry_updates: bool | None
    ipv6_retry_updates_interval: PositiveInt | None
    ipv6_update_dns_on_lease_renewal: bool | None
    ddns_domainname: str | None
    leases_per_client_settings: LeasePerClientSettingsEnum | None
    ignore_client_identifier: bool | None
    v6_leases_scavenging_enabled: bool | None
    v6_leases_scavenging_grace_period: PositiveInt | None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class NetworkView(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    networkview: str = Field(
        "networkview",
        frozen=True,
        alias="header-networkview",
        description="Default header for networkview",
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    networkcontainer: str = Field(
        "networkcontainer",
        frozen=True,
        alias="header-networkcontainer",
        description="Default header for networkcontainer",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV custom import action "
    )
    address: IPv4Address = Field(..., description="IP Address of the network container")
    netmask: IPv4Address = Field(..., description="Subnet mask address of the network container")
    comment: Optional[str] = Field(None, description="Optional comment")
    lease_time: Optional[int] = Field(None, description="DHCP lease time option in seconds")
    routers: Optional[str] = Field(None, description="List of routers option")
    domain_name: Optional[str] = Field(None, description="domain-name option")
    domain_name_servers: Optional[str] = Field(None, description="domain-name-servers option")
    broadcast_address: Optional[IPv4Address] = Field(None, description="Broadcast address option")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS Updates flag")
    ddns_domainname: Optional[str] = Field(None, description="DDNS domain name option")
    ddns_ttl: Optional[int] = Field(None, description="DDNS TTL option")
    ddns_generate_hostname: Optional[bool] = Field(None, description="DDNS generate hostname flag")
    update_static_leases: Optional[bool] = Field(None, description="DDNS Update static leases flag")
    enable_option81: Optional[bool] = Field(None, description="Enable option81 flag")
    update_dns_on_lease_renewal: Optional[bool] = Field(None, description="Enable option81 flag")
    enable_dhcp_thresholds: Optional[bool] = Field(None, description="Enable DHCP thresholds flag")
    enable_email_warnings: Optional[bool] = Field(None, description="Enable email warnings flag")
    enable_snmp_warnings: Optional[bool] = Field(None, description="Enable SNMP warnings flag")
    threshold_email_addresses: Optional[List[str]] = Field(
        None, description="List of email addresses to send warnings"
    )
    pxe_lease_time: Optional[int] = Field(None, description="PXE DHCP lease time option in seconds")
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    boot_file: Optional[str] = Field(None, description="Legacy boot-file option")
    boot_server: Optional[str] = Field(None, description="Legacy boot-server option")
    next_server: Optional[str] = Field(None, description="Legacy next-server option")
    option_logic_filters: Optional[list[str]] = Field(
        None, description="List of option logic filters"
    )
    lease_scavenge_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease scavenge time option in seconds"
    )
    is_authoritative: Optional[bool] = Field(None, description="DHCP authoritative flag")
    recycle_leases: Optional[bool] = Field(None, description="Recycle leases flag")
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options flag"
    )
    network_view: Optional[str] = Field(None, description="Network view")
    rir_organization: Optional[str] = Field(None, description="RIR organization")
    rir_registration_status: Optional[str] = Field(None, description="RIR registration status")
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: Optional[bool] = Field(None, description="Enable discovery flag")
    discovery_member: Optional[str] = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: Optional[List[IPv4Address]] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    remove_subnets: Optional[bool] = Field(
        None,
        description="Remove subnets flag, specify False to keep subnets or True to remove them."
    )

    def add_property(self, prop: str, value: str):
        if (
                prop.startswith("OPTION-")
                or prop.startswith("EA-")
                or prop.startswith("ADMGRP-")
        ):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class IPv4Network(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    network: str = Field(
        "network",
        frozen=True,
        alias="header-network",
        description="Default header for network"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV custom import action"
    )
    address: IPv4Address = Field(..., description="IP Address of the network")
    netmask: IPv4Address = Field(..., description="Subnet mask address of the network")
    rir_organization: Optional[str] = Field(None, description="RIR Organization name")
    rir_registration_status: Optional[str] = Field(None, description="RIR Registration status")
    network_view: Optional[str] = Field(None, description="Network view")
    enable_discovery: Optional[bool] = Field(None, description="Enable discovery flag")
    discovery_member: Optional[str] = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: Optional[List[IPv4Address]] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    auto_create_reversezone: Optional[bool] = Field(
        None, description="Auto create reverse zone flag"
    )
    is_authoritative: Optional[bool] = Field(None, description="DHCP authoritative flag")
    option_logic_filters: Optional[List[str]] = Field(
        None, description="List of option logic filters"
    )
    boot_file: Optional[str] = Field(None, description="Legacy boot-file option")
    boot_server: Optional[str] = Field(None, description="Legacy boot-server option")
    ddns_domainname: Optional[str] = Field(None, description="DDNS domain name option")
    generate_hostname: Optional[bool] = Field(None, description="Generate hostname flag")
    always_update_dns: Optional[bool] = Field(None, description="Always update DNS flag")
    update_static_leases: Optional[bool] = Field(None, description="Update static leases flag")
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ddns_ttl: Optional[int] = Field(None, description="DDNS TTL option in seconds")
    enable_option81: Optional[bool] = Field(None, description="Enable option81 flag")
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    broadcast_address: Optional[IPv4Address] = Field(None, description="Broadcast address option")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    enable_thresholds: Optional[bool] = Field(None, description="Enable thresholds flag")
    enable_threshold_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    range_high_water_mark: Optional[int] = Field(None, description="Range high water mark option")
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options flag"
    )
    range_low_water_mark: Optional[int] = Field(None, description="Range low water mark option")
    next_server: Optional[str] = Field(None, description="Next server option")
    lease_time: Optional[int] = Field(None, description="DHCP lease time option in seconds")
    enable_pxe_lease_time: Optional[bool] = Field(None, description="Enable PXE lease time flag")
    pxe_lease_time: Optional[int] = Field(None, description="DHCP lease time option in seconds")
    recycle_leases: Optional[bool] = Field(None, description="Recycle leases flag")
    threshold_email_addresses: Optional[list[str]] = Field(
        None, description="Email addresses to send warnings"
    )
    dhcp_members: Optional[str] = Field(None, description="DHCP members")
    routers: Optional[str] = Field(None, description="DHCP routers option")
    domain_name: Optional[str] = Field(None, description="DHCP option domain-name")
    domain_name_servers: Optional[str] = Field(None, description="DHCP option domain-name-servers")
    zone_associations: Optional[List[str]] = Field(
        None, description="List of DNS zone associations"
    )
    vlans: Optional[str] = Field(None, description="VLAN assignments - Example: default/1/4094/1")

    # OPTION-# string where the name implies DHCP vendor class
    # OPTION-XXXX-# string where XXXX implies custom vendor class
    # ea_site: str | None = Field(alias='EA-Site', default=None)
    # EA-XXX
    # EAInherited-XXX string where ea is inherited attr
    # EA-Users string example of a user-defined attr
    # ADMGRP-XXX string example of an admin group for permissions
    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6networkcontainer: str = Field(
        "ipv6networkcontainer",
        frozen=True,
        alias="header-ipv6networkcontainer",
        description="Default header for IPv6 network container"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv6Address
    cidr: PositiveInt = Field(ge=0, le=128, default=64)
    network_view: str | None = None
    comment: str | None = None
    zone_associations: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    recycle_leases: bool | None = None
    enable_ddns: bool | None = None
    ddns_domainname: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    always_update_dns: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    rir_organization: str | None = None
    rir_registration_status: str | None = None
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    remove_subnets: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6Network(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6network: str = Field(
        "ipv6network",
        frozen=True,
        alias="header-ipv6network",
        description="Default header for IPv6 network"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address: IPv6Address
    cidr: PositiveInt = Field(ge=0, le=128, default=64)
    comment: str | None = None
    network_view: str | None = None
    enable_discovery: bool | None = False
    discovery_member: str | None = None
    discovery_exclusion_range: List[IPv4Address] | None = None
    disabled: bool | None = None
    auto_create_reversezone: bool | None = False
    zone_associations: str | None = None
    dhcp_members: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    recycle_leases: bool | None = None
    enable_ddns: bool | None = None
    always_update_dns: bool | None = None
    ddns_domainname: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    vlans: str | None = None  # Example: default/1/4094/1
    rir_organization: str | None = None
    rir_registration_status: str | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited--")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4SharedNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    sharednetwork: str = Field(
        "sharednetwork",
        frozen=True,
        alias="header-sharednetwork",
        description="Default header for sharednetwork"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    networks: str
    network_view: str | None = None
    is_authoritative: bool | None = None
    option_logic_filters: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    comment: str | None = None
    generate_hostname: bool | None = None
    always_update_dns: bool | None = None
    update_static_leases: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    ddns_ttl: PositiveInt | None = None
    enable_option81: bool | None = None
    deny_bootp: bool | None = None
    disabled: bool | None = None
    enable_ddns: bool | None = None
    ignore_client_requested_options: bool | None = None
    next_server: str | None = None
    lease_time: PositiveInt | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: PositiveInt | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6SharedNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6sharednetwork: str = Field(
        "ipv6sharednetwork",
        frozen=True,
        alias="header-ipv6sharednetwork",
        description="Default header for IPv6 shared network"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    networks: str
    network_view: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None
    enable_ddns: bool | None = None
    always_update_dns: bool | None = None
    ddns_domain_name: str | None = None
    ddns_ttl: PositiveInt | None = None
    generate_hostname: bool | None = None
    update_dns_on_lease_renewal: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4DhcpRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcprange: str = Field(
        "dhcprange",
        frozen=True,
        alias="header-dhcprange",
        description="Default header for dhcprange"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    start_address: IPv4Address
    new_start_address: IPv4Address | None = Field(
        alias="_new_start_address", default=None
    )
    end_address: IPv4Address
    new_end_address: IPv4Address | None = Field(alias="_new_end_address", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    is_authoritative: bool | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    ddns_domainname: str | None = None
    generate_hostname: bool | None = None
    deny_all_clients: bool | None = None
    deny_bootp: bool | None = None
    disabled: bool | None = None
    domain_name_servers: str | None = None
    enable_ddns: bool | None = None
    enable_thresholds: bool | None = None
    enable_threshold_email_warnings: bool | None = None
    enable_threshold_snmp_warnings: bool | None = None
    threshold_email_addresses: str | None = None
    range_high_water_mark: int | None = None
    ignore_client_requested_options: bool | None = None
    range_low_water_mark: int | None = None
    next_server: str | None = None
    lease_time: int | None = None
    enable_pxe_lease_time: bool | None = None
    pxe_lease_time: int | None = None
    unknown_clients_option: str | None = None  # Example: 'Allow'
    known_clients_option: str | None = None  # Example: 'Deny'
    recycle_leases: bool | None = None
    update_dns_on_lease_renewal: bool | None = None
    always_update_dns: bool | None = None
    exclusion_ranges: str | None = (
        None  # Example: “10.1.0.200-10.1.0.254/’The range for printers’,10.2.3.3-10.2.3.30/”
    )
    member: str | None = None
    server_association_type: ServerAssociationTypeEnum | None = None
    failover_association: str | None = None
    broadcast_address: IPv4Address | None = None
    routers: str | None = None
    domain_name: str | None = None
    option_logic_filters: List[str] | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6DhcpRange(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6dhcprange: str = Field(
        "ipv6dhcprange",
        frozen=True,
        alias="header-ipv6dhcprange",
        description="Default header for IPv6 dhcprange"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address_type: IPv6AddressTypeEnum | None = None
    parent: str | None = None  # Required when address_type = PREFIX
    start_address: IPv6Address
    new_start_address: IPv6Address | None = Field(alias="_new_start_address", default=None)
    end_address: IPv6Address
    new_end_address: IPv6Address | None = Field(alias="_new_end_address", default=None)
    ipv6_start_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_start_prefix: PositiveInt | None = Field(alias="_new_ipv6_start_prefix", default=None)
    ipv6_end_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_end_prefix: PositiveInt | None = Field(alias="_new_ipv6_end_prefix", default=None)
    ipv6_prefix_bits: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix_bits: PositiveInt | None = Field(alias="_new_ipv6_prefix_bits", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    member: str | None = None
    server_association_type: ServerAssociationTypeEnum | None = None
    exclusion_ranges: str | None = None
    recycle_leases: bool | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4FixedAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    header_fixedaddress: str = Field(
        "fixedaddress",
        frozen=True,
        alias="header-fixedaddress",
        description="Default header for IPv4 fixed address"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    ip_address: IPv4Address
    ms_server: IPv4Address | None = None
    new_ip_address: IPv4Address | None = Field(alias="_new_ip_address", default=None)
    network_view: str | None = None
    name: str | None = None
    always_update_dns: bool | None = None
    option_logic_filters: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    prepared_zero: bool | None = None
    comment: str | None = None
    ddns_domainname: str | None = None
    deny_bootp: bool | None = None
    broadcast_address: IPv4Address | None = None
    routers: str | None = None
    domain_name: str | None = None
    domain_name_servers: str | None = None
    dhcp_client_identifier: str | None = None
    disabled: bool | None = None
    enable_ddns: bool | None = None
    ignore_client_requested_options: bool | None = None
    circuit_id: str | None = None
    remote_id: str | None = None
    mac_address: str | None = None
    match_option: MatchOptionEnum | None = None  # MAC_ADDRESS, CLIENT_ID, CIRCUIT_ID, REMOTE_ID
    next_server: str | None = None
    lease_time: int | None = None
    enable_pxe_lease_time: bool | None = None
    ddns_hostname: str | None = None
    pxe_lease_time: int | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv6FixedAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6fixedaddress: str = Field(
        "ipv6fixedaddress",
        frozen=True,
        alias="header-ipv6fixedaddress",
        description="Default header for IPv6 fixed address"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    address_type: IPv6AddressTypeEnum | None = None
    parent: str | None = None
    ip_address: IPv6Address
    new_ip_address: IPv6Address | None = Field(alias="_new_ip_address", default=None)
    ipv6_prefix: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix: PositiveInt | None = Field(alias="_new_ipv6_prefix", default=None)
    ipv6_prefix_bits: PositiveInt | None = Field(ge=0, le=128, default=None)
    new_ipv6_prefix_bits: PositiveInt | None = Field(alias="_new_ipv6_prefix_bits", default=None)
    network_view: str | None = None
    name: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    match_option: str | None = 'DUID'
    duid: str
    domain_name: str | None = None
    domain_name_servers: str | None = None
    valid_lifetime: PositiveInt | None = None
    preferred_lifetime: PositiveInt | None = None

    def add_property(self, code: str, value: str):
        if (
                code.startswith("OPTION-")
                or code.startswith("EA-")
                or code.startswith("EAInherited-")
                or code.startswith("ADMGRP-")
        ):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpFingerprint(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpfingerprint: str = Field(
        "dhcpfingerprint",
        frozen=True,
        alias="header-dhcpfingerprint",
        description="Default header for DHCP fingerprint"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    type: FingerprintTypeEnum | None = Field(default=FingerprintTypeEnum.CUSTOM)
    comment: str | None = None
    disable: bool | None = None
    vendor_id: str | None = None
    option_sequence: str | None = None  # Example: "['1,3,6,7,12,15,28,40,41,42,225,226,227,22/ipv4']"
    device_class: str | None = None
    protocol: ProtocolTypeEnum

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpMacFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpmacfilter: str = Field(
        "dhcpmacfilter",
        frozen=True,
        alias="header-dhcpmacfilter",
        description="Default header for dhcpmacfilter"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    never_expires: bool | None = None
    expiration_interval: PositiveInt | None = None
    enforce_expiration_time: bool | None = None
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class MacFilterAddress(BaseModel):
    model_config = ConfigDict(extra="allow")

    macfilteraddress: str = Field(
        "macfilteraddress",
        frozen=True,
        alias="header-macfilteraddress",
        description="Default header for macfilteraddress"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    mac_address: str
    new_mac_address: str | None = Field(alias="_new_mac_address", default=None)
    is_registered_user: bool | None = None
    registered_user: str | None = None
    guest_first_name: str | None = None
    guest_middle_name: str | None = None
    guest_last_name: str | None = None
    guest_email: str | None = None
    guest_phone: str | None = None
    guest_custom_field1: str | None = None
    guest_custom_field2: str | None = None
    guest_custom_field3: str | None = None
    guest_custom_field4: str | None = None
    never_expires: bool | None = None
    expire_time: datetime | None = None
    comment: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class OptionFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    optionfilter: str = Field(
        "optionfilter",
        frozen=True,
        alias="header-optionfilter",
        description="Default header for optionfilter"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    name: str
    new_name: str | None = Field(alias="_new_name", default=None)
    comment: str | None = None
    expression: str | None = None
    boot_file: str | None = None
    boot_server: str | None = None
    lease_time: int | None = None
    pxe_lease_time: int | None = None
    next_server: str | None = None
    option_space: str | None = None

    def add_property(self, code: str, value: str):
        if code.startswith("OPTION-") or code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class OptionFilterMatchRule(BaseModel):
    model_config = ConfigDict(extra="allow")

    optionfiltermatchrule: str = Field(
        "optionfiltermatchrule",
        frozen=True,
        alias="header-optionfiltermatchrule",
        description="CSV Header for optionfiltermatchrule",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="Custom CSV Import action"
    )
    parent: str = Field(..., description="Parent option filter")
    match_option: Optional[str] = Field(None, description="Option filter match option")
    match_value: Optional[str] = Field(None, description="Option filter match value")
    new_match_value: Optional[str] = Field(
        None, alias="_new_match_value", description="New option filter match value"
    )
    comment: Optional[str] = Field(None, description="Option filter match comment")
    is_substring: Optional[bool] = Field(
        None, description="Is option filter match substring"
    )
    substring_offset: Optional[int] = Field(None, description="Substring offset")
    substring_length: Optional[int] = Field(None, description="Substring length")


class RelayAgentFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    relayagentfilter: str = Field(
        "relayagentfilter",
        frozen=True,
        alias="header-relayagentfilter",
        description="The header of the relayagentfilter",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="Custom CSV import action"
    )
    name: str = Field(..., description="The name of the relay agent filter")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="The new name of the relay agent filter"
    )
    comment: Optional[str] = Field(None, description="The comment of the relay agent filter")
    circuit_id_rule: Optional[str] = Field(
        None, description="The circuit id rule of the relay agent filter"
    )
    circuit_id: Optional[str] = Field(None, description="The circuit id of the relay agent filter")
    remote_id_rule: Optional[str] = Field(
        None,
        description="The remote id rule of the relay agent filter"
    )
    remote_id: Optional[str] = Field(None, description="The remote id of the relay agent filter")

    def add_property(self, code: str, value: str):
        if code.startswith("EA-") or code.startswith("ADMGRP-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class DhcpFingerprintFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    dhcpfingerprintfilter: str = Field(
        "dhcpfingerprintfilter",
        frozen=True,
        alias="header-dhcpfingerprintfilter",
        description="Header for dhcpfingerprintfilter",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="Custom CSV import action"
    )
    name: str = Field(..., description="DHCP Fingerprint Filter name")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="New DHCP Fingerprint Filter name"
    )
    fingerprint: Optional[str] = Field(None, description="DHCP Fingerprint")
    new_fingerprint: Optional[str] = Field(None, alias="_new_fingerprint")
    comment: Optional[str] = Field(None, description="Optional comment")

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4OptionSpace(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    optionspace: str = Field(
        "optionspace",
        alias="header-optionspace",
        frozen=True,
        description="Header for optionspace"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV Custom import action"
    )
    name: str = Field(..., description="Name of the IPv4 optionspace")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="New name of the optionspace"
    )
    comment: Optional[str] = Field(None, description="Comment for the optionspace")

    @model_validator(mode="after")
    def check_alphanumeric(self) -> Self:
        if not re.match(r"\w+", self.name):
            raise ValueError("The name of an optionspace MUST be alphanumeric.")
        return self


class IPv4OptionDefinition(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    optiondefinition: str = Field(
        "optiondefinition",
        frozen=True,
        alias="header-optiondefinition",
        description="Header for optiondefinition"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV Custom import action"
    )
    space: str = Field(..., description="IPv4 DHCP Option Space")
    new_space: Optional[str] = Field(
        None, alias="_new_space", description="New name of the optionspace"
    )
    name: str = Field(..., description="IPv4 DHCP Option name")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="New IPv4 DHCP Option name"
    )
    code: str = Field(..., description="IPv4 DHCP option code number")
    type: DhcpTypeEnum = Field(..., description="DHCP option type enumeration")


class IPv6Optionspace(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ipv6optionspace: str = Field(
        'ipv6optionspace',
        frozen=True,
        alias="header-ipv6optionspace",
        description="Header for ipv6optionspace"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV Custom import action"
    )
    name: str = Field(..., description="Name of the IPv6 optionspace")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="New name of the optionspace"
    )
    comment: Optional[str] = Field(None, description="Comment for the optionspace")
    ipv6_enterprise_number: Optional[PositiveInt] = Field(
        None, description="Enterprise number for IPv6 options"
    )


class IPv6OptionDefinition(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ipv6optiondefinition: str = Field(
        'ipv6optiondefinition',
        frozen=True,
        alias="header-ipv6optiondefinition",
        description="Header for ipv6optiondefinition"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV Custom import action"
    )
    space: str = Field(..., description="IPv6 DHCP Option Space")
    new_space: Optional[str] = Field(
        None, alias="_new_space", description="New name of the optionspace"
    )
    name: str = Field(..., description="IPv6 DHCP Option name")
    new_name: Optional[str] = Field(None, alias="_new_name")
    code: str = Field(..., description="IPv6 DHCP option code number")
    type: DhcpTypeEnum = Field(..., description="DHCP option type enumeration")


class DhcpFailoverAssociation(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    dhcpfailoverassociation: str = Field(
        'dhcpfailoverassociation',
        frozen=True,
        alias="header-dhcpfailoverassociation",
        description="Header for dhcpfailoverassociation object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, alias="import-action", description="CSV Custom import action"
    )
    name: str = Field(..., description="Name of the DHCP failover association")
    new_name: Optional[str] = Field(
        None, alias="_new_name", description="New name of the DHCP failover association"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    primary_server_type: FailoverServerType = Field(..., description="Primary server type")
    grid_primary: Optional[str] = Field(None, description="Primary Grid Member FQDN")
    external_primary: Optional[str] = Field(None, description="Primary External Server FQDN")
    secondary_server_type: FailoverServerType = Field(..., description="Secondary server type")
    grid_secondary: Optional[str] = Field(None, description="Secondary Grid Member FQDN")
    external_secondary: Optional[str] = Field(None, description="Secondary External Server FQDN")
    failover_port: Optional[PositiveInt] = Field(647, gt=0, lt=63999)
    max_response_delay: Optional[PositiveInt] = Field(60, ge=1)
    mclt: Optional[PositiveInt] = Field(3600, ge=0, le=4294967295)
    max_load_balance_delay: Optional[PositiveInt] = Field(3, ge=0, le=4294967295)
    load_balance_split: Optional[PositiveInt] = Field(128, ge=0, le=255)
    recycle_leases: Optional[bool] = Field(None, description="Recycle leases flag")

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")
