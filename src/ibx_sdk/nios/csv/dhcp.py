import re
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
    PositiveInt,
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    authority: Optional[bool] = Field(None, description="DHCP Authority flag")
    domain_name: Optional[str] = Field(
        None, description="Option domain-name option"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    ignore_dhcp_option_list_request: Optional[bool] = Field(
        None, description="Ignore DHCP option list request flag"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: Optional[PositiveInt] = Field(
        None, description="PXE lease time option in seconds"
    )
    bootfile: Optional[str] = Field(None, description="Legacy boot-file option")
    bootserver: Optional[str] = Field(
        None, description="Legacy boot-server option"
    )
    nextserver: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    ddns_use_option81: Optional[bool] = Field(
        None, description="Enable option81 flag"
    )
    ddns_server_always_updates: Optional[bool] = Field(
        None, description="DNS server always updates flag"
    )
    ddns_generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    retry_ddns_updates: Optional[bool] = Field(
        None, description="Retry DDNS updates flag"
    )
    ddns_retry_interval: Optional[PositiveInt] = Field(
        None, description="Retry DDNS updates interval in seconds"
    )
    enable_dhcp_thresholds: Optional[bool] = Field(
        None, description="Enable DHCP thresholds flag"
    )
    high_water_mark: Optional[PositiveInt] = Field(
        None, description="High water mark option"
    )
    high_water_mark_reset: Optional[PositiveInt] = Field(
        None, description="High water mark reset option"
    )
    low_water_mark: Optional[PositiveInt] = Field(
        None, description="Low water mark option"
    )
    low_water_mark_reset: Optional[PositiveInt] = Field(
        None, description="Low water mark reset option"
    )
    enable_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    email_list: Optional[str] = Field(
        None, description="Email addresses to send warnings"
    )
    ipv6_domain_name_servers: Optional[str] = Field(
        None, description="IPv6 domain name servers option"
    )
    ping_count: Optional[PositiveInt] = Field(
        None, description="Ping count option"
    )
    ping_timeout: Optional[PositiveInt] = Field(
        None, description="Ping timeout option in seconds"
    )
    capture_hostname: Optional[bool] = Field(
        None, description="Capture hostname flag"
    )
    enable_leasequery: Optional[bool] = Field(
        None, description="Enable leasequery flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ipv6_update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    txt_record_handling: Optional[str] = Field(
        None, description="TXT record handling option"
    )
    lease_scavenge_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease scavenge time"
    )
    failover_port: Optional[PositiveInt] = Field(
        None, description="Failover port option"
    )
    enable_fingerprint: Optional[bool] = Field(
        None, description="enable DHCP fingerprint flag"
    )
    ipv6_enable_ddns: Optional[bool] = Field(
        None, description="Enable DDNS flag"
    )
    ipv6_enable_option_fqdn: Optional[bool] = Field(
        None, description="Enable option fqdn flag"
    )
    ipv6_ddns_server_always_updates: Optional[bool] = Field(
        None, description="Enable DDNS server always updates flag"
    )
    ipv6_generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    ipv6_ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    ipv6_ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
        None, description="Preferred lifetime option"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option"
    )
    ipv6_domain_name: Optional[str] = Field(
        None, description="IPv6 domain name option"
    )
    ipv6_txt_record_handling: Optional[str] = Field(
        None, description="IPv6 TXT record handling option"
    )
    ipv6_capture_hostname: Optional[bool] = Field(
        None, description="Capture hostname flag"
    )
    ipv6_recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    ipv6_enable_retry_updates: Optional[bool] = Field(
        None, description="Enable retry updates flag"
    )
    ipv6_retry_updates_interval: Optional[PositiveInt] = Field(
        None, description="Retry updates interval"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    leases_per_client_settings: Optional[LeasePerClientSettingsEnum] = Field(
        None, description="DHCP Leases per client settings"
    )
    ignore_client_identifier: Optional[bool] = Field(
        None, description="Ignore client identifier flag"
    )
    disable_all_nac_filters: Optional[bool] = Field(
        None, description="Disable all NAC filters flag"
    )
    format_log_option_82: Optional[bool] = Field(
        None, description="Format log option 82 flag"
    )
    v6_leases_scavenging_enabled: Optional[bool] = Field(
        None, description="Enable IPv6 leases scavenging flag"
    )
    v6_leases_scavenging_grace_period: Optional[PositiveInt] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    broadcast_address: Optional[IPv4Address] = Field(
        None, description="Broadcast address option"
    )
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options"
    )
    pxe_lease_time: Optional[PositiveInt] = Field(
        None, description="PXE lease time option"
    )
    lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option"
    )
    domain_name: Optional[str] = Field(None, description="Domain name option")
    routers: Optional[str] = Field(None, description="Routers option")
    option_logic_filters: Optional[list[str]] = Field(
        None, description="List of option logic filters"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    bootfile: Optional[str] = Field(None, description="Legacy bootfile option")
    bootserver: Optional[str] = Field(
        None, description="Legacy bootserver option"
    )
    nextserver: Optional[str] = Field(None, description="Next server option")
    enable_thresholds: Optional[bool] = Field(
        None, description="Enable thresholds flag"
    )
    range_high_water_mark: Optional[PositiveInt] = Field(
        None, description="Range high water mark option"
    )
    range_high_water_mark_reset: Optional[PositiveInt] = Field(
        None, description="Range high water mark reset option"
    )
    range_low_water_mark: Optional[PositiveInt] = Field(
        None, description="Range low water mark option"
    )
    range_low_water_mark_reset: Optional[PositiveInt] = Field(
        None, description="Range low water mark reset option"
    )
    enable_threshold_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: Optional[list[str]] = Field(
        None, description="Email addresses to send warnings"
    )
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    ddns_use_option81: Optional[bool] = Field(
        None, description="Use option81 flag"
    )
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    update_static_leases: Optional[bool] = Field(
        None, description="Update static leases flag"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
        None, description="Preferred lifetime option in seconds"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option in seconds"
    )
    name: str = Field(..., description="DHCP member name")
    is_authoritative: Optional[bool] = Field(
        None, description="DHCP authoritative flag"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    ping_count: Optional[int] = Field(None, description="Ping count")
    ping_timeout: Optional[int] = Field(None, description="Ping timeout")
    enable_leasequery: Optional[bool] = Field(
        None, description="Enable lease query flag"
    )
    retry_ddns_updates: Optional[bool] = Field(
        None, description="Enable DDNS updates flag"
    )
    ddns_retry_interval: Optional[int] = Field(
        None, description="DDNS retry interval option in seconds"
    )
    lease_scavenge_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease scavenge time option in seconds"
    )
    enable_fingerprint: Optional[bool] = Field(
        None, description="Enable fingerprint detection flag"
    )
    ipv6_enable_ddns: Optional[bool] = Field(
        None, description="Enable IPv6 DDNS flag"
    )
    ipv6_ddns_enable_option_fqdn: Optional[bool] = Field(
        None, description="Enable IPv6 DDNS FQDN flag"
    )
    ipv6_generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    ipv6_ddns_domainname: Optional[str] = Field(
        None, description="IPv6 DDNS domain name option"
    )
    ipv6_ddns_ttl: Optional[PositiveInt] = Field(
        None, description="IPv6 DDNS TTL option in seconds"
    )
    ipv6_domain_name_servers: Optional[str] = Field(
        None, description="IPv6 domain name servers option"
    )
    ipv6_domain_name: Optional[str] = Field(
        None, description="IPv6 domain name option"
    )
    ipv6_recycle_leases: Optional[bool] = Field(
        None, description="Recycle IPv6 leases flag"
    )
    ipv6_server_duid: Optional[str] = Field(
        None, description="IPv6 server DUID option"
    )
    ipv6_enable_retry_updates: Optional[bool] = Field(
        None, description="Enable IPv6 retry updates flag"
    )
    ipv6_retry_updates_interval: Optional[int] = Field(
        None, description="IPv6 retry updates interval option in seconds"
    )
    ipv6_update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="IPv6 update DNS on lease renewal flag"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    leases_per_client_settings: Optional[LeasePerClientSettingsEnum] = Field(
        None, description="Leases per client settings"
    )
    ignore_client_identifier: Optional[bool] = Field(
        None, description="Ignore client identifier flag"
    )
    v6_leases_scavenging_enabled: Optional[bool] = Field(
        None, description="IPv6 lease scavenging enabled flag"
    )
    v6_leases_scavenging_grace_period: Optional[int] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Network view name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New network view name",
    )
    comment: Optional[str] = Field(None, description="Optional comment")

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
    import_action: Optional[ImportActionEnum] = Field(
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
    comment: Optional[str] = Field(None, description="Optional comment")
    lease_time: Optional[int] = Field(
        None, description="DHCP lease time option in seconds"
    )
    routers: Optional[str] = Field(None, description="List of routers option")
    domain_name: Optional[str] = Field(None, description="domain-name option")
    domain_name_servers: Optional[str] = Field(
        None, description="domain-name-servers option"
    )
    broadcast_address: Optional[IPv4Address] = Field(
        None, description="Broadcast address option"
    )
    enable_ddns: Optional[bool] = Field(
        None, description="Enable DDNS Updates flag"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: Optional[int] = Field(None, description="DDNS TTL option")
    ddns_generate_hostname: Optional[bool] = Field(
        None, description="DDNS generate hostname flag"
    )
    update_static_leases: Optional[bool] = Field(
        None, description="DDNS Update static leases flag"
    )
    enable_option81: Optional[bool] = Field(
        None, description="Enable option81 flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Enable option81 flag"
    )
    enable_dhcp_thresholds: Optional[bool] = Field(
        None, description="Enable DHCP thresholds flag"
    )
    enable_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: Optional[List[str]] = Field(
        None, description="List of email addresses to send warnings"
    )
    pxe_lease_time: Optional[int] = Field(
        None, description="PXE DHCP lease time option in seconds"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    boot_file: Optional[str] = Field(
        None, description="Legacy boot-file option"
    )
    boot_server: Optional[str] = Field(
        None, description="Legacy boot-server option"
    )
    next_server: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    option_logic_filters: Optional[list[str]] = Field(
        None, description="List of option logic filters"
    )
    lease_scavenge_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease scavenge time option in seconds"
    )
    is_authoritative: Optional[bool] = Field(
        None, description="DHCP authoritative flag"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options flag"
    )
    network_view: Optional[str] = Field(None, description="Network view")
    rir_organization: Optional[str] = Field(
        None, description="RIR organization"
    )
    rir_registration_status: Optional[str] = Field(
        None, description="RIR registration status"
    )
    # last_rir_registration_update_sent: str | None = None # Read-only
    # last_rir_registration_update_status: str | None = None # Read-only
    enable_discovery: Optional[bool] = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: Optional[str] = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: Optional[List[IPv4Address]] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    remove_subnets: Optional[bool] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv4Address = Field(..., description="IP Address of the network")
    netmask: IPv4Address = Field(
        ..., description="Subnet mask address of the network"
    )
    rir_organization: Optional[str] = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: Optional[str] = Field(
        None, description="RIR Registration status"
    )
    network_view: Optional[str] = Field(None, description="Network view")
    enable_discovery: Optional[bool] = Field(
        None, description="Enable discovery flag"
    )
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
    is_authoritative: Optional[bool] = Field(
        None, description="DHCP authoritative flag"
    )
    option_logic_filters: Optional[List[str]] = Field(
        None, description="List of option logic filters"
    )
    boot_file: Optional[str] = Field(
        None, description="Legacy boot-file option"
    )
    boot_server: Optional[str] = Field(
        None, description="Legacy boot-server option"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    update_static_leases: Optional[bool] = Field(
        None, description="Update static leases flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ddns_ttl: Optional[int] = Field(
        None, description="DDNS TTL option in seconds"
    )
    enable_option81: Optional[bool] = Field(
        None, description="Enable option81 flag"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    broadcast_address: Optional[IPv4Address] = Field(
        None, description="Broadcast address option"
    )
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    enable_thresholds: Optional[bool] = Field(
        None, description="Enable thresholds flag"
    )
    enable_threshold_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    range_high_water_mark: Optional[int] = Field(
        None, description="Range high water mark option"
    )
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options flag"
    )
    range_low_water_mark: Optional[int] = Field(
        None, description="Range low water mark option"
    )
    next_server: Optional[str] = Field(None, description="Next server option")
    lease_time: Optional[int] = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: Optional[int] = Field(
        None, description="DHCP lease time option in seconds"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    threshold_email_addresses: Optional[list[str]] = Field(
        None, description="Email addresses to send warnings"
    )
    dhcp_members: Optional[List[str]] = Field(None, description="DHCP members")
    routers: Optional[str] = Field(None, description="DHCP routers option")
    domain_name: Optional[str] = Field(
        None, description="DHCP option domain-name"
    )
    domain_name_servers: Optional[str] = Field(
        None, description="DHCP option domain-name-servers"
    )
    zone_associations: Optional[List[str]] = Field(
        None, description="List of DNS zone associations"
    )
    vlans: Optional[str] = Field(
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
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer(
        "option_logic_filters", "dhcp_members", when_used="always"
    )
    def serialize_list_fields(
        self, values: Optional[List[str]]
    ) -> Optional[str]:
        return self.list_to_csv(values)


class IPv6NetworkContainer(BaseModel):
    model_config = ConfigDict(extra="allow")

    ipv6networkcontainer: str = Field(
        "ipv6networkcontainer",
        frozen=True,
        serialization_alias="header-ipv6networkcontainer",
        description="Default header for IPv6 network container",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv6Address = Field(..., description="IP Address of the network")
    cidr: PositiveInt = Field(
        ..., ge=0, le=128, description="CIDR mask address of the network"
    )
    network_view: Optional[str] = Field(None, description="Network view")
    comment: Optional[str] = Field(None, description="Optional comment")
    zone_associations: Optional[str] = Field(
        None, description="List of DNS zone associations"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
        None, description="Preferred lifetime option in seconds"
    )
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    rir_organization: Optional[str] = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: Optional[str] = Field(
        None, description="RIR Registration status"
    )
    enable_discovery: Optional[bool] = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: Optional[str] = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: Optional[List[IPv4Address]] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    remove_subnets: Optional[bool] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address: IPv6Address = Field(..., description="IPv Address of the network")
    cidr: PositiveInt = Field(
        ..., ge=0, le=128, description="CIDR mask address of the network"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    network_view: Optional[str] = Field(None, description="Network view")
    enable_discovery: Optional[bool] = Field(
        None, description="Enable discovery flag"
    )
    discovery_member: Optional[str] = Field(
        None, description="Discovery member name if discovery is enabled"
    )
    discovery_exclusion_range: Optional[List[IPv6Address]] = Field(
        None, description="List of IP Ranges to be excluded from discovery"
    )
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    auto_create_reversezone: Optional[bool] = Field(
        None, description="Auto create reverse zone flag"
    )
    zone_associations: Optional[List[str]] = Field(
        None, description="List of DNS zone associations"
    )
    dhcp_members: Optional[str] = Field(None, description="DHCP members")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
        None, description="Preferred lifetime option in seconds"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="Domain name option"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal"
    )
    vlans: Optional[str] = Field(
        None, description="VLAN assignments - Example: default/1/4094/1"
    )
    rir_organization: Optional[str] = Field(
        None, description="RIR Organization name"
    )
    rir_registration_status: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Shared network name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New shared network name",
    )
    networks: List[str] = Field(..., description="List of networks")
    network_view: Optional[str] = Field(None, description="Network view")
    is_authoritative: Optional[bool] = Field(
        None, description="Is authoritative flag"
    )
    option_logic_filters: Optional[List[str]] = Field(
        None, description="List of option logic filters"
    )
    boot_file: Optional[str] = Field(None, description="Legacy bootfile option")
    boot_server: Optional[str] = Field(
        None, description="Legacy bootserver option"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    update_static_leases: Optional[bool] = Field(
        None, description="Update static leases flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal flag"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    enable_option81: Optional[bool] = Field(None, description="Enable option81")
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options"
    )
    next_server: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option in seconds"
    )
    routers: Optional[str] = Field(None, description="DHCP routers option")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Shared network name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New shared network name",
    )
    networks: List[str] = Field(..., description="List of networks")
    network_view: Optional[str] = Field(None, description="Network view")
    comment: Optional[str] = Field(None, description="Optional comment")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name option"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
        None, description="Preferred lifetime option in seconds"
    )
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    ddns_domain_name: Optional[str] = Field(
        None, description="DDNS domain name option"
    )
    ddns_ttl: Optional[PositiveInt] = Field(
        None, description="DDNS TTL option in seconds"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    start_address: IPv4Address = Field(
        ..., description="DHCP range start address"
    )
    new_start_address: Optional[IPv4Address] = Field(
        None,
        serialization_alias="_new_start_address",
        description="New DHCP range start address",
    )
    end_address: IPv4Address = Field(..., description="DHCP range end address")
    new_end_address: Optional[IPv4Address] = Field(
        None,
        serialization_alias="_new_end_address",
        description="New DHCP range end address",
    )
    network_view: Optional[str] = Field(None, description="Network view")
    name: Optional[str] = Field(None, description="DHCP range name")
    comment: Optional[str] = Field(None, description="Optional comment")
    is_authoritative: Optional[bool] = Field(
        None, description="Is authoritative flag"
    )
    boot_file: Optional[str] = Field(None, description="Legacy bootfile option")
    boot_server: Optional[str] = Field(
        None, description="Legacy bootserver option"
    )
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS Domain name option"
    )
    generate_hostname: Optional[bool] = Field(
        None, description="Generate hostname flag"
    )
    deny_all_clients: Optional[bool] = Field(
        None, description="Deny all clients flag"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    enable_thresholds: Optional[bool] = Field(
        None, description="Enable thresholds flag"
    )
    enable_threshold_email_warnings: Optional[bool] = Field(
        None, description="Enable email warnings flag"
    )
    enable_threshold_snmp_warnings: Optional[bool] = Field(
        None, description="Enable SNMP warnings flag"
    )
    threshold_email_addresses: Optional[list[str]] = Field(
        None, description="Email addresses to send warnings"
    )
    range_high_water_mark: Optional[int] = Field(
        None, description="Range high water mark option"
    )
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options flag"
    )
    range_low_water_mark: Optional[int] = Field(
        None, description="Range low water mark option"
    )
    next_server: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    pxe_lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option in seconds"
    )
    unknown_clients_option: Optional[str] = Field(
        None, description="Unknown clients option"
    )
    known_clients_option: Optional[str] = Field(
        None, description="Known clients option"
    )
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )
    update_dns_on_lease_renewal: Optional[bool] = Field(
        None, description="Update DNS on lease renewal"
    )
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    exclusion_ranges: Optional[List[str]] = Field(
        None,
        description="List of exclusion ranges in 'start-end/comment' format",
    )
    member: Optional[str] = Field(None, description="DHCP member name")
    server_association_type: Optional[ServerAssociationTypeEnum] = Field(
        None,
        description="DHCP server association type MEMBER, FAILOVER, or NONE",
    )
    failover_association: Optional[str] = Field(
        None, description="DHCP failover association name"
    )
    broadcast_address: Optional[IPv4Address] = Field(
        None, description="DHCP broadcast address option"
    )
    routers: Optional[list] = Field(None, description="List of routers")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    option_logic_filters: Optional[List[str]] = Field(
        None, description="List of option logic filters"
    )

    @field_serializer("exclusion_ranges", when_used="always")
    def serialize_exclusion_ranges(self, exclusion_ranges: str):
        if self.exclusion_ranges is None:
            return None
        return ",".join(self.exclusion_ranges)

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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address_type: Optional[IPv6AddressTypeEnum] = Field(
        None, description="IPv6 address type option"
    )
    parent: Optional[str] = Field(None, description="Parent v6 block")
    start_address: IPv6Address = Field(
        ..., description="DHCP range start address"
    )
    new_start_address: Optional[IPv6Address] = Field(
        None,
        serialization_alias="_new_start_address",
        description="New DHCP range start address",
    )
    end_address: IPv6Address = Field(..., description="DHCP range end address")
    new_end_address: Optional[IPv6Address] = Field(
        None,
        serialization_alias="_new_end_address",
        description="New DHCP range end address",
    )
    ipv6_start_prefix: Optional[PositiveInt] = Field(
        None, ge=0, le=128, description="IPv6 start prefix option"
    )
    new_ipv6_start_prefix: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_ipv6_start_prefix",
        description="New IPv6 start prefix",
    )
    ipv6_end_prefix: Optional[PositiveInt] = Field(
        None, ge=0, le=128, description="IPv6 end prefix option"
    )
    new_ipv6_end_prefix: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_ipv6_end_prefix",
        description="New IPv6 end prefix",
    )
    ipv6_prefix_bits: Optional[PositiveInt] = Field(
        None, ge=0, le=128, description="IPv6 prefix bits option"
    )
    new_ipv6_prefix_bits: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_ipv6_prefix_bits",
        description="New IPv6 prefix bits",
    )
    network_view: Optional[str] = Field(None, description="Network view")
    name: Optional[str] = Field(None, description="DHCP range name")
    comment: Optional[str] = Field(None, description="Optional comment")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    member: Optional[str] = Field(None, description="DHCP member name")
    server_association_type: Optional[ServerAssociationTypeEnum] = Field(
        None, description="DHCP server association type MEMBER, or NONE"
    )
    exclusion_ranges: Optional[List[str]] = Field(
        None,
        description="List of exclusion ranges in 'start-end/comment' format",
    )
    recycle_leases: Optional[bool] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    ip_address: IPv4Address = Field(..., description="IP address")
    ms_server: Optional[IPv4Address] = Field(None, description="MS server name")
    new_ip_address: Optional[IPv4Address] = Field(
        None,
        serialization_alias="_new_ip_address",
        description="New IP address of fixed address",
    )
    network_view: Optional[str] = Field(None, description="Network view")
    name: Optional[str] = Field(None, description="Fixed address name")
    always_update_dns: Optional[bool] = Field(
        None, description="Always update DNS flag"
    )
    option_logic_filters: Optional[List[str]] = Field(
        None, description="List of option logic filters"
    )
    boot_file: Optional[str] = Field(None, description="Legacy bootfile option")
    boot_server: Optional[str] = Field(
        None, description="Legacy bootserver option"
    )
    prepared_zero: Optional[bool] = Field(
        None, description="Prepared zero flag"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    ddns_domainname: Optional[str] = Field(
        None, description="DDNS Domain name option"
    )
    deny_bootp: Optional[bool] = Field(None, description="Deny bootp flag")
    broadcast_address: Optional[IPv4Address] = Field(
        None, description="Broadcast address option"
    )
    routers: Optional[str] = Field(None, description="List of routers")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    dhcp_client_identifier: Optional[str] = Field(
        None, description="DHCP client identifier option"
    )
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    enable_ddns: Optional[bool] = Field(None, description="Enable DDNS flag")
    ignore_client_requested_options: Optional[bool] = Field(
        None, description="Ignore client requested options"
    )
    circuit_id: Optional[str] = Field(None, description="Circuit ID option")
    remote_id: Optional[str] = Field(None, description="Remote ID option")
    mac_address: Optional[str] = Field(None, description="MAC address option")
    match_option: Optional[MatchOptionEnum] = Field(
        None, description="Match option"
    )
    next_server: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    lease_time: Optional[PositiveInt] = Field(
        None, description="DHCP lease time option in seconds"
    )
    enable_pxe_lease_time: Optional[bool] = Field(
        None, description="Enable PXE lease time flag"
    )
    ddns_hostname: Optional[str] = Field(
        None, description="DDNS hostname option"
    )
    pxe_lease_time: Optional[PositiveInt] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    address_type: Optional[IPv6AddressTypeEnum] = Field(
        None, description="IPv6 address type option"
    )
    parent: Optional[IPv6Network] = Field(None, description="Parent v6 block")
    ip_address: IPv6Address = Field(..., description="IP address")
    new_ip_address: Optional[IPv6Address] = Field(
        None,
        serialization_alias="_new_ip_address",
        description="New IP address of fixed address",
    )
    ipv6_prefix: Optional[PositiveInt] = Field(
        None, ge=0, le=128, description="IPv6 prefix option"
    )
    new_ipv6_prefix: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_ipv6_prefix",
        description="New IPv6 prefix",
    )
    ipv6_prefix_bits: Optional[PositiveInt] = Field(
        None, ge=0, le=128, description="IPv6 prefix bits option"
    )
    new_ipv6_prefix_bits: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_ipv6_prefix_bits",
        description="New IPv6 prefix bits",
    )
    network_view: Optional[str] = Field(None, description="Network view")
    name: Optional[str] = Field(None, description="Fixed address name")
    comment: Optional[str] = Field(None, description="Optional comment")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    match_option: Optional[str] = Field("DUID", description="Match option")
    duid: str = Field(..., description="DUID string")
    domain_name: Optional[str] = Field(None, description="Domain name option")
    domain_name_servers: Optional[str] = Field(
        None, description="Domain name servers option"
    )
    valid_lifetime: Optional[PositiveInt] = Field(
        None, description="Valid lifetime option in seconds"
    )
    preferred_lifetime: Optional[PositiveInt] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="DHCP Fingerprint name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name for DHCP Fingerprint",
    )
    type: Optional[FingerprintTypeEnum] = Field(
        FingerprintTypeEnum.CUSTOM, description="DHCP Fingerprint type"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    disable: Optional[bool] = Field(None, description="Disabled flag")
    vendor_id: Optional[str] = Field(None, description="Vendor ID string")
    option_sequence: Optional[str] = Field(
        None, description="Option sequence ['1,2,3/ipv4']"
    )
    device_class: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="DHCP Mac filter name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name for DHCP Mac filter",
    )
    never_expires: Optional[bool] = Field(
        None, description="Never expires flag"
    )
    expiration_interval: Optional[PositiveInt] = Field(
        None, description="Expiration interval option"
    )
    enforce_expiration_time: Optional[bool] = Field(
        None, description="Enforce expiration time flag"
    )
    comment: Optional[str] = Field(None, description="Optional comment")

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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    parent: str = Field(..., description="Mac Filter name")
    mac_address: str = Field(..., description="MAC address")
    new_mac_address: Optional[str] = Field(
        None,
        serialization_alias="_new_mac_address",
        description="New MAC address",
    )
    is_registered_user: Optional[bool] = Field(
        None, description="Is registered user flag"
    )
    registered_user: Optional[str] = Field(
        None, description="Registered user name"
    )
    guest_first_name: Optional[str] = Field(
        None, description="Guest first name"
    )
    guest_middle_name: Optional[str] = Field(
        None, description="Guest middle name"
    )
    guest_last_name: Optional[str] = Field(None, description="Guest last name")
    guest_email: Optional[str] = Field(None, description="Guest email")
    guest_phone: Optional[str] = Field(None, description="Guest phone")
    guest_custom_field1: Optional[str] = Field(
        None, description="Guest custom field 1"
    )
    guest_custom_field2: Optional[str] = Field(
        None, description="Guest custom field 2"
    )
    guest_custom_field3: Optional[str] = Field(
        None, description="Guest custom field 3"
    )
    guest_custom_field4: Optional[str] = Field(
        None, description="Guest custom field 4"
    )
    never_expires: Optional[bool] = Field(
        None, description="Never expires flag"
    )
    expire_time: Optional[datetime] = Field(
        None, description="Expiration time option"
    )
    comment: Optional[str] = Field(None, description="Optional comment")

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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV custom import action",
    )
    name: str = Field(..., description="Option filter name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name for Option filter",
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    expression: Optional[str] = Field(None, description="Expression")
    boot_file: Optional[str] = Field(None, description="Legacy bootfile option")
    boot_server: Optional[str] = Field(
        None, description="Legacy bootserver option"
    )
    lease_time: Optional[int] = Field(
        None, description="DHCP lease time option in seconds"
    )
    pxe_lease_time: Optional[int] = Field(
        None, description="DHCP lease time option in seconds"
    )
    next_server: Optional[str] = Field(
        None, description="Legacy next-server option"
    )
    option_space: Optional[str] = Field(None, description="Option space")

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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV Import action",
    )
    parent: str = Field(..., description="Parent option filter")
    match_option: Optional[str] = Field(
        None, description="Option filter match option"
    )
    match_value: Optional[str] = Field(
        None, description="Option filter match value"
    )
    new_match_value: Optional[str] = Field(
        None,
        serialization_alias="_new_match_value",
        description="New option filter match value",
    )
    comment: Optional[str] = Field(
        None, description="Option filter match comment"
    )
    is_substring: Optional[bool] = Field(
        None, description="Is option filter match substring"
    )
    substring_offset: Optional[int] = Field(
        None, description="Substring offset"
    )
    substring_length: Optional[int] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV import action",
    )
    name: str = Field(..., description="The name of the relay agent filter")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="The new name of the relay agent filter",
    )
    comment: Optional[str] = Field(
        None, description="The comment of the relay agent filter"
    )
    circuit_id_rule: Optional[str] = Field(
        None, description="The circuit id rule of the relay agent filter"
    )
    circuit_id: Optional[str] = Field(
        None, description="The circuit id of the relay agent filter"
    )
    remote_id_rule: Optional[str] = Field(
        None, description="The remote id rule of the relay agent filter"
    )
    remote_id: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="Custom CSV import action",
    )
    name: str = Field(..., description="DHCP Fingerprint Filter name")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New DHCP Fingerprint Filter name",
    )
    fingerprint: Optional[str] = Field(None, description="DHCP Fingerprint")
    new_fingerprint: Optional[str] = Field(
        None, serialization_alias="_new_fingerprint"
    )
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
        serialization_alias="header-optionspace",
        frozen=True,
        description="Header for optionspace",
    )
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the IPv4 optionspace")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the optionspace",
    )
    comment: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    space: str = Field(..., description="IPv4 DHCP Option Space")
    new_space: Optional[str] = Field(
        None,
        serialization_alias="_new_space",
        description="New name of the optionspace",
    )
    name: str = Field(..., description="IPv4 DHCP Option name")
    new_name: Optional[str] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the IPv6 optionspace")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the optionspace",
    )
    comment: Optional[str] = Field(
        None, description="Comment for the optionspace"
    )
    ipv6_enterprise_number: Optional[PositiveInt] = Field(
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    space: str = Field(..., description="IPv6 DHCP Option Space")
    new_space: Optional[str] = Field(
        None,
        serialization_alias="_new_space",
        description="New name of the optionspace",
    )
    name: str = Field(..., description="IPv6 DHCP Option name")
    new_name: Optional[str] = Field(None, serialization_alias="_new_name")
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
    import_action: Optional[ImportActionEnum] = Field(
        None,
        serialization_alias="import-action",
        description="CSV Custom import action",
    )
    name: str = Field(..., description="Name of the DHCP failover association")
    new_name: Optional[str] = Field(
        None,
        serialization_alias="_new_name",
        description="New name of the DHCP failover association",
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    primary_server_type: FailoverServerTypeEnum = Field(
        ..., description="Primary server type"
    )
    grid_primary: Optional[str] = Field(
        None, description="Primary Grid Member FQDN"
    )
    external_primary: Optional[str] = Field(
        None, description="Primary External Server FQDN"
    )
    secondary_server_type: FailoverServerTypeEnum = Field(
        ..., description="Secondary server type"
    )
    grid_secondary: Optional[str] = Field(
        None, description="Secondary Grid Member FQDN"
    )
    external_secondary: Optional[str] = Field(
        None, description="Secondary External Server FQDN"
    )
    failover_port: Optional[PositiveInt] = Field(647, gt=0, lt=63999)
    max_response_delay: Optional[PositiveInt] = Field(60, ge=1)
    mclt: Optional[PositiveInt] = Field(3600, ge=0, le=4294967295)
    max_load_balance_delay: Optional[PositiveInt] = Field(
        3, ge=0, le=4294967295
    )
    load_balance_split: Optional[PositiveInt] = Field(128, ge=0, le=255)
    recycle_leases: Optional[bool] = Field(
        None, description="Recycle leases flag"
    )

    def add_property(self, code: str, value: str):
        if code.startswith("EA-"):
            self.__setattr__(code, value)
        else:
            raise Exception(f"Invalid field name: {code}")
