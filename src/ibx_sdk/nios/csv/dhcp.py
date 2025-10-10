import re
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import List

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
    field_serializer,
)
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
    FailoverServerTypeEnum,
)


class GridDhcp(BaseModel):
    model_config = ConfigDict(extra="allow")

    griddhcp: str = Field(
        "griddhcp",
        frozen=True,
        serialization_alias="header-griddhcp",
        description="Default header for griddhcp",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    authority: bool | None = Field(None, description="DHCP Authority flag")
    domain_name: str | None = Field(
        None, description="Option domain-name option"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    ignore_dhcp_option_list_request: bool | None = Field(
        None, description="Ignore DHCP option list request flag"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: int | None = Field(
        None, description="PXE lease time option in seconds"
    )
    bootfile: str | None = Field(None, description="Legacy boot-file option")
    bootserver: str | None = Field(
        None, description="Legacy boot-server option"
    )
    nextserver: str | None = Field(
        None, description="Legacy next-server option"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    ddns_use_option81: bool | None = Field(
        None, description="Enable option81 flag"
    )
    ddns_server_always_updates: bool | None = Field(
        None, description="DNS server always updates flag"
    )
    ddns_generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    retry_ddns_updates: bool | None = Field(
        None, description="Retry DDNS updates flag"
    )
    ddns_retry_interval: int | None = Field(
        None, description="Retry DDNS updates interval in seconds"
    )
    enable_dhcp_thresholds: bool | None = Field(
        None, description="Enable DHCP thresholds flag"
    )
    high_water_mark: int | None = Field(
        None, description="High water mark option"
    )
    high_water_mark_reset: int | None = Field(
        None, description="High water mark reset option"
    )
    low_water_mark: int | None = Field(
        None, description="Low water mark option"
    )
    low_water_mark_reset: int | None = Field(
        None, description="Low water mark reset option"
    )
    enable_email_warnings: bool | None = Field(
        None, description="Enable email warnings flag"
    )
    enable_snmp_warnings: bool | None = Field(
        None, description="Enable SNMP warnings flag"
    )
    email_list: str | None = Field(
        None, description="Email addresses to send warnings"
    )
    ipv6_domain_name_servers: str | None = Field(
        None, description="IPv6 domain name servers option"
    )
    ping_count: int | None = Field(
        None, description="Ping count option"
    )
    ping_timeout: int | None = Field(
        None, description="Ping timeout option in seconds"
    )
    capture_hostname: bool | None = Field(
        None, description="Capture hostname flag"
    )
    enable_leasequery: bool | None = Field(
        None, description="Enable leasequery flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ipv6_update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    txt_record_handling: str | None = Field(
        None, description="TXT record handling option"
    )
    lease_scavenge_time: int | None = Field(
        None, description="DHCP lease scavenge time"
    )
    failover_port: int | None = Field(
        None, description="Failover port option"
    )
    enable_fingerprint: bool | None = Field(
        None, description="enable DHCP fingerprint flag"
    )
    ipv6_enable_ddns: bool | None = Field(
        None, description="Enable DDNS flag"
    )
    ipv6_enable_option_fqdn: bool | None = Field(
        None, description="Enable option fqdn flag"
    )
    ipv6_ddns_server_always_updates: bool | None = Field(
        None, description="Enable DDNS server always updates flag"
    )
    ipv6_generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    ipv6_ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    ipv6_ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option"
    )
    ipv6_domain_name: str | None = Field(
        None, description="IPv6 domain name option"
    )
    ipv6_txt_record_handling: str | None = Field(
        None, description="IPv6 TXT record handling option"
    )
    ipv6_capture_hostname: bool | None = Field(
        None, description="Capture hostname flag"
    )
    ipv6_recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    ipv6_enable_retry_updates: bool | None = Field(
        None, description="Enable retry updates flag"
    )
    ipv6_retry_updates_interval: int | None = Field(
        None, description="Retry updates interval"
    )
    ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    leases_per_client_settings: LeasePerClientSettingsEnum | None = Field(
        None, description="DHCP Leases per client settings"
    )
    ignore_client_identifier: bool | None = Field(
        None, description="Ignore client identifier flag"
    )
    disable_all_nac_filters: bool | None = Field(
        None, description="Disable all NAC filters flag"
    )
    format_log_option_82: bool | None = Field(
        None, description="Format log option 82 flag"
    )
    v6_leases_scavenging_enabled: bool | None = Field(
        None, description="Enable IPv6 leases scavenging flag"
    )
    v6_leases_scavenging_grace_period: int | None = Field(
        None, description="IPv6 leases scavenging grace period option"
    )

    def add_property(self, code: str, value: str) -> None:
        if code.startswith("OPTION-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class MemberDhcp(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    memberdhcp: str = Field(
        "memberdhcp",
        frozen=True,
        serialization_alias="header-memberdhcp",
        description="Default header for memberdhcp",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    broadcast_address: IPv4Address | None = Field(
        None, description="Broadcast address option"
    )
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options"
    )
    pxe_lease_time: int | None = Field(
        None, description="PXE lease time option"
    )
    lease_time: int | None = Field(
        None, description="DHCP lease time option"
    )
    domain_name: str | None = Field(None, description="Domain name option")
    routers: str | None = Field(None, description="Routers option")
    option_logic_filters: list[str | None] = Field(
        None, description="List of option logic filters"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    bootfile: str | None = Field(None, description="Legacy bootfile option")
    bootserver: str | None = Field(
        None, description="Legacy bootserver option"
    )
    nextserver: str | None = Field(None, description="Next server option")
    enable_thresholds: bool | None = Field(
        None, description="Enable thresholds flag"
    )
    range_high_water_mark: int | None = Field(
        None, description="Range high water mark option"
    )
    range_high_water_mark_reset: int | None = Field(
        None, description="Range high water mark reset option"
    )
    range_low_water_mark: int | None = Field(
        None, description="Range low water mark option"
    )
    range_low_water_mark_reset: int | None = Field(
        None, description="Range low water mark reset option"
    )
    enable_threshold_email_warnings: bool | None = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: bool | None = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: list[str | None] = Field(
        None, description="Email addresses to send warnings"
    )
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    ddns_use_option81: bool | None = Field(
        None, description="Use option81 flag"
    )
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    update_static_leases: bool | None = Field(
        None, description="Update static leases flag"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option in seconds"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option in seconds"
    )
    name: str = Field(..., description="DHCP member name")
    is_authoritative: bool | None = Field(
        None, description="DHCP authoritative flag"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    ping_count: int | None = Field(None, description="Ping count")
    ping_timeout: int | None = Field(None, description="Ping timeout")
    enable_leasequery: bool | None = Field(
        None, description="Enable lease query flag"
    )
    retry_ddns_updates: bool | None = Field(
        None, description="Enable DDNS updates flag"
    )
    ddns_retry_interval: int | None = Field(
        None, description="DDNS retry interval option in seconds"
    )
    lease_scavenge_time: int | None = Field(
        None, description="DHCP lease scavenge time option in seconds"
    )
    enable_fingerprint: bool | None = Field(
        None, description="Enable fingerprint detection flag"
    )
    ipv6_enable_ddns: bool | None = Field(
        None, description="Enable IPv6 DDNS flag"
    )
    ipv6_ddns_enable_option_fqdn: bool | None = Field(
        None, description="Enable IPv6 DDNS FQDN flag"
    )
    ipv6_generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    ipv6_ddns_domainname: str | None = Field(
        None, description="IPv6 DDNS domain name option"
    )
    ipv6_ddns_ttl: int | None = Field(
        None, description="IPv6 DDNS TTL option in seconds"
    )
    ipv6_domain_name_servers: str | None = Field(
        None, description="IPv6 domain name servers option"
    )
    ipv6_domain_name: str | None = Field(
        None, description="IPv6 domain name option"
    )
    ipv6_recycle_leases: bool | None = Field(
        None, description="Recycle IPv6 leases flag"
    )
    ipv6_server_duid: str | None = Field(
        None, description="IPv6 server DUID option"
    )
    ipv6_enable_retry_updates: bool | None = Field(
        None, description="Enable IPv6 retry updates flag"
    )
    ipv6_retry_updates_interval: int | None = Field(
        None, description="IPv6 retry updates interval option in seconds"
    )
    ipv6_update_dns_on_lease_renewal: bool | None = Field(
        None, description="IPv6 update DNS on lease renewal flag"
    )
    ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    leases_per_client_settings: LeasePerClientSettingsEnum | None = Field(
        None, description="Leases per client settings"
    )
    ignore_client_identifier: bool | None = Field(
        None, description="Ignore client identifier flag"
    )
    v6_leases_scavenging_enabled: bool | None = Field(
        None, description="IPv6 lease scavenging enabled flag"
    )
    v6_leases_scavenging_grace_period: int | None = Field(
        None, description="IPv6 lease scavenging grace period option in seconds"
    )

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
        serialization_alias="header-networkview",
        description="Default header for networkview",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Network view name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New network view name",
    )
    comment: str | None = Field(None, description="Optional comment")

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
        serialization_alias="header-networkcontainer",
        description="Default header for networkcontainer",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action ",
    )
    address: IPv4Address = Field(
        ..., description="IP Address of the network container"
    )
    netmask: IPv4Address = Field(
        ..., description="Subnet mask address of the network container"
    )
    comment: str | None = Field(None, description="Optional comment")
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    routers: str | None = Field(None, description="List of routers option")
    domain_name: str | None = Field(None, description="domain-name option")
    domain_name_servers: str | None = Field(
        None, description="domain-name-servers option"
    )
    broadcast_address: IPv4Address | None = Field(
        None, description="Broadcast address option"
    )
    enable_ddns: bool | None = Field(
        None, description="Enable DDNS Updates flag"
    )
    ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: int | None = Field(None, description="DDNS TTL option")
    ddns_generate_hostname: bool | None = Field(
        None, description="DDNS generate hostname flag"
    )
    update_static_leases: bool | None = Field(
        None, description="DDNS Update static leases flag"
    )
    enable_option81: bool | None = Field(
        None, description="Enable option81 flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Enable option81 flag"
    )
    enable_dhcp_thresholds: bool | None = Field(
        None, description="Enable DHCP thresholds flag"
    )
    enable_email_warnings: bool | None = Field(
        None, description="Enable email warnings flag"
    )
    enable_snmp_warnings: bool | None = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: List[str | None] = Field(
        None, description="List of email addresses to send warnings"
    )
    pxe_lease_time: int | None = Field(
        None, description="PXE DHCP lease time option in seconds"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    boot_file: str | None = Field(
        None, description="Legacy boot-file option"
    )
    boot_server: str | None = Field(
        None, description="Legacy boot-server option"
    )
    next_server: str | None = Field(
        None, description="Legacy next-server option"
    )
    option_logic_filters: list[str | None] = Field(
        None, description="List of option logic filters"
    )
    lease_scavenge_time: int | None = Field(
        None, description="DHCP lease scavenge time option in seconds"
    )
    is_authoritative: bool | None = Field(
        None, description="DHCP authoritative flag"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options flag"
    )
    network_view: str | None = Field(None, description="Network view")
    rir_organization: str | None = Field(
        None, description="RIR organization"
    )
    rir_registration_status: str | None = Field(
        None, description="RIR registration status"
    )
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: bool | None = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: str | None = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: List[IPv4Address | None] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    remove_subnets: bool | None = Field(
        None,
        description="Remove subnets flag, specify False to keep subnets or True to remove them.",
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
        serialization_alias="header-network",
        description="Default header for network",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv4Address = Field(..., description="IP Address of the network")
    netmask: IPv4Address = Field(
        ..., description="Subnet mask address of the network"
    )
    rir_organization: str | None = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: str | None = Field(
        None, description="RIR Registration status"
    )
    network_view: str | None = Field(None, description="Network view")
    enable_discovery: bool | None = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: str | None = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: List[IPv4Address | None] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    comment: str | None = Field(None, description="Optional comment")
    auto_create_reversezone: bool | None = Field(
        None, description="Auto create reverse zone flag"
    )
    is_authoritative: bool | None = Field(
        None, description="DHCP authoritative flag"
    )
    option_logic_filters: List[str | None] = Field(
        None, description="List of option logic filters"
    )
    boot_file: str | None = Field(
        None, description="Legacy boot-file option"
    )
    boot_server: str | None = Field(
        None, description="Legacy boot-server option"
    )
    ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    update_static_leases: bool | None = Field(
        None, description="Update static leases flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    enable_option81: bool | None = Field(
        None, description="Enable option81 flag"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    broadcast_address: IPv4Address | None = Field(
        None, description="Broadcast address option"
    )
    disabled: bool | None = Field(None, description="Disabled flag")
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    enable_thresholds: bool | None = Field(
        None, description="Enable thresholds flag"
    )
    enable_threshold_email_warnings: bool | None = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: bool | None = Field(
        None, description="Enable SNMP warnings flag"
    )
    range_high_water_mark: int | None = Field(
        None, description="Range high water mark option"
    )
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options flag"
    )
    range_low_water_mark: int | None = Field(
        None, description="Range low water mark option"
    )
    next_server: str | None = Field(None, description="Next server option")
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    threshold_email_addresses: list[str | None] = Field(
        None, description="Email addresses to send warnings"
    )
    dhcp_members: List[str | None] = Field(None, description="DHCP members")
    routers: str | None = Field(None, description="DHCP routers option")
    domain_name: str | None = Field(
        None, description="DHCP option domain-name"
    )
    domain_name_servers: str | None = Field(
        None, description="DHCP option domain-name-servers"
    )
    zone_associations: List[str | None] = Field(
        None, description="List of DNS zone associations"
    )
    vlans: str | None = Field(
        None, description="VLAN assignments - Example: default/1/4094/1"
    )

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

    @staticmethod
    def list_to_csv(items: List[str | None]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer(
        "option_logic_filters", "dhcp_members", when_used="always"
    )
    def serialize_list_fields(
        self, values: List[str | None]
    ) -> str | None:
        return self.list_to_csv(values)


class IPv6NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6networkcontainer: str = Field(
        "ipv6networkcontainer",
        frozen=True,
        serialization_alias="header-ipv6networkcontainer",
        description="Default header for IPv6 network container",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv6Address = Field(..., description="IP Address of the network")
    cidr: int = Field(
        ..., ge=0, le=128, description="CIDR mask address of the network"
    )
    network_view: str | None = Field(None, description="Network view")
    comment: str | None = Field(None, description="Optional comment")
    zone_associations: str | None = Field(
        None, description="List of DNS zone associations"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option in seconds"
    )
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    ddns_domainname: str | None = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    rir_organization: str | None = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: str | None = Field(
        None, description="RIR Registration status"
    )
    enable_discovery: bool | None = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: str | None = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: List[IPv4Address | None] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    remove_subnets: bool | None = Field(
        None, description="Remove subnets flag"
    )

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
        serialization_alias="header-ipv6network",
        description="Default header for IPv6 network",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv6Address = Field(..., description="IPv Address of the network")
    cidr: int = Field(
        ..., ge=0, le=128, description="CIDR mask address of the network"
    )
    comment: str | None = Field(None, description="Optional comment")
    network_view: str | None = Field(None, description="Network view")
    enable_discovery: bool | None = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: str | None = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: List[IPv6Address | None] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    disabled: bool | None = Field(None, description="Disabled flag")
    auto_create_reversezone: bool | None = Field(
        None, description="Auto create reverse zone flag"
    )
    zone_associations: List[str | None] = Field(
        None, description="List of DNS zone associations"
    )
    dhcp_members: str | None = Field(None, description="DHCP members")
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option in seconds"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    ddns_domainname: str | None = Field(
        None, description="Domain name option"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal"
    )
    vlans: str | None = Field(
        None, description="VLAN assignments - Example: default/1/4094/1"
    )
    rir_organization: str | None = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: str | None = Field(
        None, description="RIR Registration status"
    )

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


class IPv4SharedNetwork(BaseModel):
    model_config = ConfigDict(extra="allow")

    sharednetwork: str = Field(
        "sharednetwork",
        frozen=True,
        serialization_alias="header-sharednetwork",
        description="Default header for sharednetwork",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Shared network name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New shared network name",
    )
    networks: List[str] = Field(..., description="List of networks")
    network_view: str | None = Field(None, description="Network view")
    is_authoritative: bool | None = Field(
        None, description="Is authoritative flag"
    )
    option_logic_filters: List[str | None] = Field(
        None, description="List of option logic filters"
    )
    boot_file: str | None = Field(None, description="Legacy bootfile option")
    boot_server: str | None = Field(
        None, description="Legacy bootserver option"
    )
    comment: str | None = Field(None, description="Optional comment")
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    update_static_leases: bool | None = Field(
        None, description="Update static leases flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    enable_option81: bool | None = Field(None, description="Enable option81")
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    disabled: bool | None = Field(None, description="Disabled flag")
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options"
    )
    next_server: str | None = Field(
        None, description="Legacy next-server option"
    )
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    routers: str | None = Field(None, description="DHCP routers option")
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )

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
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    ipv6sharednetwork: str = Field(
        "ipv6sharednetwork",
        frozen=True,
        serialization_alias="header-ipv6sharednetwork",
        description="Default header for IPv6 shared network",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Shared network name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New shared network name",
    )
    networks: List[str] = Field(..., description="List of networks")
    network_view: str | None = Field(None, description="Network view")
    comment: str | None = Field(None, description="Optional comment")
    disabled: bool | None = Field(None, description="Disabled flag")
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name option"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option in seconds"
    )
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    ddns_domain_name: str | None = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: int | None = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal"
    )

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
        serialization_alias="header-dhcprange",
        description="Default header for dhcprange",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    start_address: IPv4Address = Field(
        ..., description="DHCP range start address"
    )
    new_start_address: IPv4Address | None = Field(
        None,
        serialization_alias="_new_start_address",
        description="New DHCP range start address",
    )
    end_address: IPv4Address = Field(..., description="DHCP range end address")
    new_end_address: IPv4Address | None = Field(
        None,
        serialization_alias="_new_end_address",
        description="New DHCP range end address",
    )
    network_view: str | None = Field(None, description="Network view")
    name: str | None = Field(None, description="DHCP range name")
    comment: str | None = Field(None, description="Optional comment")
    is_authoritative: bool | None = Field(
        None, description="Is authoritative flag"
    )
    boot_file: str | None = Field(None, description="Legacy bootfile option")
    boot_server: str | None = Field(
        None, description="Legacy bootserver option"
    )
    ddns_domainname: str | None = Field(
        None, description="DDNS Domain name option"
    )
    generate_hostname: bool | None = Field(
        None, description="Generate hostname flag"
    )
    deny_all_clients: bool | None = Field(
        None, description="Deny all clients flag"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    disabled: bool | None = Field(None, description="Disabled flag")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    enable_thresholds: bool | None = Field(
        None, description="Enable thresholds flag"
    )
    enable_threshold_email_warnings: bool | None = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: bool | None = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: list[str | None] = Field(
        None, description="Email addresses to send warnings"
    )
    range_high_water_mark: int | None = Field(
        None, description="Range high water mark option"
    )
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options flag"
    )
    range_low_water_mark: int | None = Field(
        None, description="Range low water mark option"
    )
    next_server: str | None = Field(
        None, description="Legacy next-server option"
    )
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    unknown_clients_option: str | None = Field(
        None, description="Unknown clients option"
    )
    known_clients_option: str | None = Field(
        None, description="Known clients option"
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )
    update_dns_on_lease_renewal: bool | None = Field(
        None, description="Update DNS on lease renewal"
    )
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    exclusion_ranges: List[str | None] = Field(
        None,
        description="List of exclusion ranges in 'start-end/comment' format",
    )
    member: str | None = Field(None, description="DHCP member name")
    server_association_type: ServerAssociationTypeEnum | None = Field(
        None,
        description="DHCP server association type MEMBER, FAILOVER, or NONE",
    )
    failover_association: str | None = Field(
        None, description="DHCP failover association name"
    )
    broadcast_address: IPv4Address | None = Field(
        None, description="DHCP broadcast address option"
    )
    routers: list | None = Field(None, description="List of routers")
    domain_name: str | None = Field(None, description="Domain name option")
    option_logic_filters: List[str | None] = Field(
        None, description="List of option logic filters"
    )

    @field_serializer("exclusion_ranges", when_used="always")
    def serialize_exclusion_ranges(self, value):
        if value is None:
            return None
        return ",".join(value)

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
        serialization_alias="header-ipv6dhcprange",
        description="Default header for IPv6 dhcprange",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address_type: IPv6AddressTypeEnum | None = Field(
        None, description="IPv6 address type option"
    )
    parent: str | None = Field(None, description="Parent v6 block")
    start_address: IPv6Address = Field(
        ..., description="DHCP range start address"
    )
    new_start_address: IPv6Address | None = Field(
        None,
        serialization_alias="_new_start_address",
        description="New DHCP range start address",
    )
    end_address: IPv6Address = Field(..., description="DHCP range end address")
    new_end_address: IPv6Address | None = Field(
        None,
        serialization_alias="_new_end_address",
        description="New DHCP range end address",
    )
    ipv6_start_prefix: int | None = Field(
        None, ge=0, le=128, description="IPv6 start prefix option"
    )
    new_ipv6_start_prefix: int | None = Field(
        None,
        serialization_alias="_new_ipv6_start_prefix",
        description="New IPv6 start prefix",
    )
    ipv6_end_prefix: int | None = Field(
        None, ge=0, le=128, description="IPv6 end prefix option"
    )
    new_ipv6_end_prefix: int | None = Field(
        None,
        serialization_alias="_new_ipv6_end_prefix",
        description="New IPv6 end prefix",
    )
    ipv6_prefix_bits: int | None = Field(
        None, ge=0, le=128, description="IPv6 prefix bits option"
    )
    new_ipv6_prefix_bits: int | None = Field(
        None,
        serialization_alias="_new_ipv6_prefix_bits",
        description="New IPv6 prefix bits",
    )
    network_view: str | None = Field(None, description="Network view")
    name: str | None = Field(None, description="DHCP range name")
    comment: str | None = Field(None, description="Optional comment")
    disabled: bool | None = Field(None, description="Disabled flag")
    member: str | None = Field(None, description="DHCP member name")
    server_association_type: ServerAssociationTypeEnum | None = Field(
        None, description="DHCP server association type MEMBER, or NONE"
    )
    exclusion_ranges: List[str | None] = Field(
        None,
        description="List of exclusion ranges in 'start-end/comment' format",
    )
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )

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
        serialization_alias="header-fixedaddress",
        description="Default header for IPv4 fixed address",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    ip_address: IPv4Address = Field(..., description="IP address")
    ms_server: IPv4Address | None = Field(None, description="MS server name")
    new_ip_address: IPv4Address | None = Field(
        None,
        serialization_alias="_new_ip_address",
        description="New IP address of fixed address",
    )
    network_view: str | None = Field(None, description="Network view")
    name: str | None = Field(None, description="Fixed address name")
    always_update_dns: bool | None = Field(
        None, description="Always update DNS flag"
    )
    option_logic_filters: List[str | None] = Field(
        None, description="List of option logic filters"
    )
    boot_file: str | None = Field(None, description="Legacy bootfile option")
    boot_server: str | None = Field(
        None, description="Legacy bootserver option"
    )
    prepared_zero: bool | None = Field(
        None, description="Prepared zero flag"
    )
    comment: str | None = Field(None, description="Optional comment")
    ddns_domainname: str | None = Field(
        None, description="DDNS Domain name option"
    )
    deny_bootp: bool | None = Field(None, description="Deny bootp flag")
    broadcast_address: IPv4Address | None = Field(
        None, description="Broadcast address option"
    )
    routers: str | None = Field(None, description="List of routers")
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    dhcp_client_identifier: str | None = Field(
        None, description="DHCP client identifier option"
    )
    disabled: bool | None = Field(None, description="Disabled flag")
    enable_ddns: bool | None = Field(None, description="Enable DDNS flag")
    ignore_client_requested_options: bool | None = Field(
        None, description="Ignore client requested options"
    )
    circuit_id: str | None = Field(None, description="Circuit ID option")
    remote_id: str | None = Field(None, description="Remote ID option")
    mac_address: str | None = Field(None, description="MAC address option")
    match_option: MatchOptionEnum | None = Field(
        None, description="Match option"
    )
    next_server: str | None = Field(
        None, description="Legacy next-server option"
    )
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: bool | None = Field(
        None, description="Enable PXE lease time flag"
    )
    ddns_hostname: str | None = Field(
        None, description="DDNS hostname option"
    )
    pxe_lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )

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
        serialization_alias="header-ipv6fixedaddress",
        description="Default header for IPv6 fixed address",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address_type: IPv6AddressTypeEnum | None = Field(
        None, description="IPv6 address type option"
    )
    parent: IPv6Network | None = Field(None, description="Parent v6 block")
    ip_address: IPv6Address = Field(..., description="IP address")
    new_ip_address: IPv6Address | None = Field(
        None,
        serialization_alias="_new_ip_address",
        description="New IP address of fixed address",
    )
    ipv6_prefix: int | None = Field(
        None, ge=0, le=128, description="IPv6 prefix option"
    )
    new_ipv6_prefix: int | None = Field(
        None,
        serialization_alias="_new_ipv6_prefix",
        description="New IPv6 prefix",
    )
    ipv6_prefix_bits: int | None = Field(
        None, ge=0, le=128, description="IPv6 prefix bits option"
    )
    new_ipv6_prefix_bits: int | None = Field(
        None,
        serialization_alias="_new_ipv6_prefix_bits",
        description="New IPv6 prefix bits",
    )
    network_view: str | None = Field(None, description="Network view")
    name: str | None = Field(None, description="Fixed address name")
    comment: str | None = Field(None, description="Optional comment")
    disabled: bool | None = Field(None, description="Disabled flag")
    match_option: str | None = Field("DUID", description="Match option")
    duid: str = Field(..., description="DUID string")
    domain_name: str | None = Field(None, description="Domain name option")
    domain_name_servers: str | None = Field(
        None, description="Domain name servers option"
    )
    valid_lifetime: int | None = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: int | None = Field(
        None, description="Preferred lifetime option in seconds"
    )

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
        serialization_alias="header-dhcpfingerprint",
        description="Default header for DHCP fingerprint",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="DHCP Fingerprint name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name for DHCP Fingerprint",
    )
    type: FingerprintTypeEnum | None = Field(
        FingerprintTypeEnum.CUSTOM, description="DHCP Fingerprint type"
    )
    comment: str | None = Field(None, description="Optional comment")
    disable: bool | None = Field(None, description="Disabled flag")
    vendor_id: str | None = Field(None, description="Vendor ID string")
    option_sequence: str | None = Field(
        None, description="Option sequence ['1,2,3/ipv4']"
    )
    device_class: str | None = Field(
        None, description="DHCP Device class used for filtering"
    )
    protocol: ProtocolTypeEnum = Field(
        ..., description="protocol can be IPV4 or IPV6"
    )

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
        serialization_alias="header-dhcpmacfilter",
        description="Default header for dhcpmacfilter",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="DHCP Mac filter name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name for DHCP Mac filter",
    )
    never_expires: bool | None = Field(
        None, description="Never expires flag"
    )
    expiration_interval: int | None = Field(
        None, description="Expiration interval option"
    )
    enforce_expiration_time: bool | None = Field(
        None, description="Enforce expiration time flag"
    )
    comment: str | None = Field(None, description="Optional comment")

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
        serialization_alias="header-macfilteraddress",
        description="Default header for macfilteraddress",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    parent: str = Field(..., description="Mac Filter name")
    mac_address: str = Field(..., description="MAC address")
    new_mac_address: str | None = Field(
        None,
        serialization_alias="_new_mac_address",
        description="New MAC address",
    )
    is_registered_user: bool | None = Field(
        None, description="Is registered user flag"
    )
    registered_user: str | None = Field(
        None, description="Registered user name"
    )
    guest_first_name: str | None = Field(
        None, description="Guest first name"
    )
    guest_middle_name: str | None = Field(
        None, description="Guest middle name"
    )
    guest_last_name: str | None = Field(None, description="Guest last name")
    guest_email: str | None = Field(None, description="Guest email")
    guest_phone: str | None = Field(None, description="Guest phone")
    guest_custom_field1: str | None = Field(
        None, description="Guest custom field 1"
    )
    guest_custom_field2: str | None = Field(
        None, description="Guest custom field 2"
    )
    guest_custom_field3: str | None = Field(
        None, description="Guest custom field 3"
    )
    guest_custom_field4: str | None = Field(
        None, description="Guest custom field 4"
    )
    never_expires: bool | None = Field(
        None, description="Never expires flag"
    )
    expire_time: datetime | None = Field(
        None, description="Expiration time option"
    )
    comment: str | None = Field(None, description="Optional comment")

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
        serialization_alias="header-optionfilter",
        description="Default header for optionfilter",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Option filter name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name for Option filter",
    )
    comment: str | None = Field(None, description="Optional comment")
    expression: str | None = Field(None, description="Expression")
    boot_file: str | None = Field(None, description="Legacy bootfile option")
    boot_server: str | None = Field(
        None, description="Legacy bootserver option"
    )
    lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    pxe_lease_time: int | None = Field(
        None, description="DHCP lease time option in seconds"
    )
    next_server: str | None = Field(
        None, description="Legacy next-server option"
    )
    option_space: str | None = Field(None, description="Option space")

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
        serialization_alias="header-optionfiltermatchrule",
        description="CSV Header for optionfiltermatchrule",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV Import action",
    )
    parent: str = Field(..., description="Parent option filter")
    match_option: str | None = Field(
        None, description="Option filter match option"
    )
    match_value: str | None = Field(
        None, description="Option filter match value"
    )
    new_match_value: str | None = Field(
        None,
        serialization_alias="_new_match_value",
        description="New option filter match value",
    )
    comment: str | None = Field(
        None, description="Option filter match comment"
    )
    is_substring: bool | None = Field(
        None, description="Is option filter match substring"
    )
    substring_offset: int | None = Field(
        None, description="Substring offset"
    )
    substring_length: int | None = Field(
        None, description="Substring length"
    )


class RelayAgentFilter(BaseModel):
    model_config = ConfigDict(extra="allow")

    relayagentfilter: str = Field(
        "relayagentfilter",
        frozen=True,
        serialization_alias="header-relayagentfilter",
        description="The header of the relayagentfilter",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV import action",
    )
    name: str = Field(..., description="The name of the relay agent filter")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="The new name of the relay agent filter",
    )
    comment: str | None = Field(
        None, description="The comment of the relay agent filter"
    )
    circuit_id_rule: str | None = Field(
        None, description="The circuit id rule of the relay agent filter"
    )
    circuit_id: str | None = Field(
        None, description="The circuit id of the relay agent filter"
    )
    remote_id_rule: str | None = Field(
        None, description="The remote id rule of the relay agent filter"
    )
    remote_id: str | None = Field(
        None, description="The remote id of the relay agent filter"
    )

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
        serialization_alias="header-dhcpfingerprintfilter",
        description="Header for dhcpfingerprintfilter",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV import action",
    )
    name: str = Field(..., description="DHCP Fingerprint Filter name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New DHCP Fingerprint Filter name",
    )
    fingerprint: str | None = Field(None, description="DHCP Fingerprint")
    new_fingerprint: str | None = Field(
        None, serialization_alias="_new_fingerprint"
    )
    comment: str | None = Field(None, description="Optional comment")

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")


class IPv4OptionSpace(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    optionspace: str = Field(
        "optionspace",
        serialization_alias="header-optionspace",
        frozen=True,
        description="Header for optionspace",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the IPv4 optionspace")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the optionspace",
    )
    comment: str | None = Field(
        None, description="Comment for the optionspace"
    )

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
        serialization_alias="header-optiondefinition",
        description="Header for optiondefinition",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    space: str = Field(..., description="IPv4 DHCP Option Space")
    new_space: str | None = Field(
        None,
        serialization_alias="_new_space",
        description="New name of the optionspace",
    )
    name: str = Field(..., description="IPv4 DHCP Option name")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New IPv4 DHCP Option name",
    )
    code: str = Field(..., description="IPv4 DHCP option code number")
    type: DhcpTypeEnum = Field(..., description="DHCP option type enumeration")


class IPv6Optionspace(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ipv6optionspace: str = Field(
        "ipv6optionspace",
        frozen=True,
        serialization_alias="header-ipv6optionspace",
        description="Header for ipv6optionspace",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the IPv6 optionspace")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the optionspace",
    )
    comment: str | None = Field(
        None, description="Comment for the optionspace"
    )
    ipv6_enterprise_number: int | None = Field(
        None, description="Enterprise number for IPv6 options"
    )


class IPv6OptionDefinition(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    ipv6optiondefinition: str = Field(
        "ipv6optiondefinition",
        frozen=True,
        serialization_alias="header-ipv6optiondefinition",
        description="Header for ipv6optiondefinition",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    space: str = Field(..., description="IPv6 DHCP Option Space")
    new_space: str | None = Field(
        None,
        serialization_alias="_new_space",
        description="New name of the optionspace",
    )
    name: str = Field(..., description="IPv6 DHCP Option name")
    new_name: str | None = Field(None, serialization_alias="_new_name")
    code: str = Field(..., description="IPv6 DHCP option code number")
    type: DhcpTypeEnum = Field(..., description="DHCP option type enumeration")


class DhcpFailoverAssociation(BaseModel):
    model_config = ConfigDict(extra="allow", use_enum_values=True)

    dhcpfailoverassociation: str = Field(
        "dhcpfailoverassociation",
        frozen=True,
        serialization_alias="header-dhcpfailoverassociation",
        description="Header for dhcpfailoverassociation object",
    )
    import_action: ImportActionEnum | None = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the DHCP failover association")
    new_name: str | None = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the DHCP failover association",
    )
    comment: str | None = Field(None, description="Optional comment")
    primary_server_type: FailoverServerTypeEnum = Field(
        ..., description="Primary server type"
    )
    grid_primary: str | None = Field(
        None, description="Primary Grid Member FQDN"
    )
    external_primary: str | None = Field(
        None, description="Primary External Server FQDN"
    )
    secondary_server_type: FailoverServerTypeEnum = Field(
        ..., description="Secondary server type"
    )
    grid_secondary: str | None = Field(
        None, description="Secondary Grid Member FQDN"
    )
    external_secondary: str | None = Field(
        None, description="Secondary External Server FQDN"
    )
    failover_port: int | None = Field(647, gt=0, lt=63999)
    max_response_delay: int | None = Field(60, ge=1)
    mclt: int | None = Field(3600, ge=0, le=4294967295)
    max_load_balance_delay: int | None = Field(
        3, ge=0, le=4294967295
    )
    load_balance_split: int | None = Field(128, ge=0, le=255)
    recycle_leases: bool | None = Field(
        None, description="Recycle leases flag"
    )

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")
