from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, PositiveInt, field_serializer, IPvAnyAddress

from .enums import ZoneFormatTypeEnum, ImportActionEnum


class MemberDns(BaseModel):
    model_config = ConfigDict(extra="allow")

    memberdns: str = Field(
        "memberdns",
        frozen=True,
        serialization_alias="header-memberdns",
        description="CSV header for memberdns"
    )
    import_action: Optional[ImportActionEnum] = Field(
        serialization_alias="import-action", default=None, description="CSV custom import action"
    )
    parent: str = Field(..., description="Parent FQDN Member")
    dns_over_mgmt: Optional[bool] = Field(None, description="DNS over management interface")
    dns_over_lan2: Optional[bool] = Field(None, description="DNS over LAN2 interface")
    minimal_response: Optional[bool] = Field(None, description="Minimal response flag")
    forwarders_only: Optional[bool] = Field(None, description="Forwarders only flag")
    allow_forwarder: Optional[List[str]] = Field(None, description="List of forwarders")
    member_view_nats: Optional[List[str]] = Field(
        None, description="List of member view NATs VIEW/INTERFACE/IP"
    )
    enable_notify_source_port: Optional[bool] = Field(None, description="Enable notify source port")
    notify_source_port: Optional[PositiveInt] = Field(None, description="Notify source port")
    enable_query_source_port: Optional[bool] = Field(None, description="Enable query source port")
    query_source_port: Optional[PositiveInt] = Field(None, description="Query source port")
    lame_ttl: Optional[PositiveInt] = Field(
        600, gt=0, lt=1800, description="Lame TTL"
    )
    auto_sort_views: Optional[bool] = Field(None, description="Auto sort views flag")
    member_views: Optional[List[str]] = Field(None, description="Member views")
    allow_transfer: Optional[List[str]] = Field(
        None, description="List of allowed transfer servers ITEM/Allow or ITEM/Deny"
    )
    excluded_servers: Optional[List[IPvAnyAddress]] = Field(
        None, description="List of excluded transfer servers"
    )
    zone_transfer_format_option: Optional[str] = Field(
        None, description="Zone transfer format option"
    )
    recursion_enabled: Optional[bool] = Field(None, description="Recursion enabled flag")
    allow_query: Optional[List[str]] = Field(None, description="List of allowed query servers")
    allow_recursive_query: Optional[List[str]] = Field(
        None, description="List of allowed recursive query servers"
    )
    limit_concurrent_recursive_clients: Optional[bool] = Field(
        None, description="Limit concurrent recursive clients flag"
    )
    concurrent_recursive_clients: Optional[PositiveInt] = Field(
        1000, description="Concurrent recursive clients"
    )
    allow_update: Optional[List[str]] = Field(None, description="List of allowed update servers")
    allow_gss_tsig_zone_updates: Optional[bool] = Field(
        None, description="Allow GSS TSIG zone updates flag"
    )
    allow_update_forwarding: Optional[bool] = Field(
        None, description="Allow update forwarding flag"
    )
    enable_custom_root_server: Optional[bool] = Field(None, description="Enable custom root server")
    root_name_servers: Optional[List[str]] = Field(
        None, description="List of custom root name servers"
    )
    enable_blackhole: Optional[bool] = Field(None, description="Enable blackhole flag")
    blackhole: Optional[List[str]] = Field(None, description="List of blackhole servers")
    notify_delay: Optional[PositiveInt] = Field(
        None, ge=5, le=86400, description="Notify delay in seconds"
    )
    enable_nxdomain_redirect: Optional[bool] = Field(
        None, description="Enable nxdomain redirect flag"
    )
    nxdomain_redirect_addresses: Optional[List[str]] = Field(
        None, description="List of nxdomain redirect addresses"
    )
    nxdomain_redirect_ttl: Optional[PositiveInt] = Field(
        None, description="TTL for nxdomain redirect"
    )
    nxdomain_log_query: Optional[bool] = Field(None, description="Enable nxdomain log query flag")
    nxdomain_rulesets: Optional[List[str]] = Field(None, description="List of nxdomain rulesets")
    enable_blacklist: Optional[bool] = Field(None, description="Enable blacklist flag")
    blacklist_redirect_addresses: Optional[List[str]] = Field(
        None, description="List of blacklist redirect addresses"
    )
    blacklist_action: Optional[str] = Field(None, description="Blacklist action i.e. Refuse")
    blacklist_redirect_ttl: Optional[PositiveInt] = Field(
        None, description="TTL for blacklist redirect"
    )
    blacklist_log_query: Optional[bool] = Field(None, description="Enable blacklist log query flag")
    blacklist_rulesets: Optional[List[str]] = Field(None, description="List of blacklist rulesets")
    enable_dns64: Optional[bool] = Field(None, description="Enable DNS64 flag")
    dns64_groups: Optional[List[str]] = Field(None, description="List of DNS64 groups")
    max_cached_lifetime: Optional[PositiveInt] = Field(
        86400, ge=60, le=86400, description="Max cached lifetime in seconds")
    dns_over_v6_mgmt: Optional[bool] = Field(None, description="DNS over v6 management interface")
    dns_over_v6_lan2: Optional[bool] = Field(None, description="DNS over v6 LAN2 interface")
    filter_aaaa: Optional[bool] = Field(None, description="Enable filter AAAA flag")
    filter_aaaa_list: Optional[List[str]] = Field(
        None,
        description="List of filter AAAA addresses '12.0.0.12/Deny,10.0.0.0/8/Allow,NACL/Allow'"
    )
    dns_over_v6_lan: Optional[bool] = Field(None, description="DNS over v6 LAN interface")
    copy_xfer_to_notify: Optional[bool] = Field(
        None, description="Enable copy transfer to notify flag"
    )
    transfers_in: Optional[PositiveInt] = Field(
        10, ge=10, le=100, description="Max transfers in"
    )
    transfers_out: Optional[PositiveInt] = Field(
        10, ge=10, le=100, description="Max transfers out"
    )
    transfers_per_ns: Optional[PositiveInt] = Field(
        None, ge=2, le=100, description="Max transfers per NS"
    )
    serial_query_rate: Optional[PositiveInt] = Field(
        20, ge=20, le=100, description="Serial query rate"
    )
    max_cache_ttl: Optional[PositiveInt] = Field(
        86400, description="Max cache TTL in seconds"
    )
    max_ncache_ttl: Optional[PositiveInt] = Field(
        10800, le=604800, description="Max ncache TTL in seconds"
    )
    disable_edns: Optional[bool] = Field(None, description="Disable EDNS flag")
    query_rewrite_enabled: Optional[bool] = Field(None, description="Enable query rewrite flag")
    rpz_drop_ip_rule_enabled: Optional[bool] = Field(
        None, description="Enable RPZ drop IP rule flag"
    )
    rpz_drop_ip_rule_min_prefix_length_ipv4: Optional[PositiveInt] = Field(
        29, ge=0, le=32, description="RPZ drop IP rule min prefix length IPv4"
    )
    rpz_drop_ip_rule_min_prefix_length_ipv6: Optional[PositiveInt] = Field(
        112, ge=0, le=128, description="RPZ drop IP rule min prefix length IPv6"
    )
    atc_forwarding_enable: Optional[bool] = Field(
        None,
        description="Enable recursive queries forwarding to Advanced DNS Threat Defense Cloud flag"
    )
    atc_forwarding_access_key: Optional[str] = Field(
        None, description="Advanced DNS Threat Defense Cloud access key"
    )
    atc_forwarding_resolver_address: Optional[IPvAnyAddress] = Field(
        None, description="Advanced DNS Threat Defense Cloud resolver address"
    )
    atc_forwarding_forward_first: Optional[bool] = Field(
        None, description="Fallback to Advanced DNS Threat Defense Cloud forward first flag"
    )

    @staticmethod
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer(
        'allow_forwarder',
        'member_view_nats',
        'member_views',
        'allow_transfer',
        'excluded_servers',
        'allow_query',
        'allow_recursive_query',
        'allow_update',
        'root_name_servers',
        'blackhole',
        'nxdomain_redirect_addresses',
        'nxdomain_rulesets',
        'blacklist_redirect_addresses',
        'blacklist_rulesets',
        'dns64_groups',
        'filter_aaaa_list',
        when_used="always"
    )
    def serialize_list_fields(self, values: Optional[List[str]]) -> Optional[str]:
        return self.list_to_csv(values)


class DnsView(BaseModel):
    model_config = ConfigDict(extra="allow")

    view: str = Field(
        'view',
        frozen=True,
        serialization_alias="header-view",
        description="CSV header for view object"
    )
    name: str = Field(..., description="View name")
    new_name: Optional[str] = Field(
        None, serialization_alias="_new_name", description="New view name"
    )
    comment: Optional[str] = Field(None, description="Optional view comment field")
    network_view: Optional[str] = Field(None, description="Network view name")
    disable: Optional[bool] = Field(None, description="Disable view flag")
    recursion: Optional[bool] = Field(None, description="Enable recursion flag")
    root_name_server_type: Optional[str] = Field(
        None, description="Root name server type, i.e. Custom"
    )
    match_clients: Optional[List[str]] = Field(
        None, description="List of clients to match [IP|NET|ACL,...]"
    )
    match_destinations: Optional[List[str]] = Field(
        None, description="List of destinations to match [IP|NET|ACL,...]"
    )
    custom_root_name_servers: Optional[List[str]] = Field(
        None, description="List of custom root name servers [FQDN/IP,...]"
    )
    lame_ttl: Optional[PositiveInt] = Field(None, description="Lame TTL value")
    nxdomain_redirect: Optional[bool] = Field(None, description="Enable NXDOMAIN redirect flag")
    nxdomain_redirect_addresses: Optional[List[str]] = Field(
        None, description="List of NXDOMAIN redirect addresses [IP,...]"
    )
    nxdomain_redirect_ttl: Optional[PositiveInt] = Field(
        None, description="NXDOMAIN redirect TTL value"
    )
    nxdomain_log_query: Optional[bool] = Field(None, description="Enable NXDOMAIN log query flag")
    nxdomain_rulesets: Optional[List[str]] = Field(
        None, description="List of NXDOMAIN rulesets [FQDNs,...]"
    )
    enable_blacklist: Optional[bool] = Field(None, description="Enable blacklist flag")
    blacklist_redirect_addresses: Optional[List[str]] = Field(
        None, description="List of blacklist redirect addresses [IP,...]"
    )
    blacklist_action: Optional[str] = Field(None, description="Blacklist action, i.e. Redirect")
    blacklist_redirect_ttl: Optional[PositiveInt] = Field(
        None, description="Blacklist redirect TTL value"
    )
    blacklist_log_query: Optional[bool] = Field(None, description="Enable blacklist log query flag")
    blacklist_rulesets: Optional[List[str]] = Field(
        None, description="List of blacklist rulesets [FQDNs,...]"
    )
    enable_dns64: Optional[bool] = Field(None, description="Enable DNS64 flag")
    dns64_groups: Optional[List[str]] = Field(None, description="List of DNS64 groups [GROUP,...]")
    forwarders_only: Optional[bool] = Field(None, description="Forwarders only flag")
    forwarders: Optional[List[str]] = Field(None, description="List of forwarders [IP,...]")
    filter_aaaa: Optional[str] = Field(None, description="Enable filter AAAA flag, i.e. Yes or No")
    filter_aaaa_list: Optional[List[str]] = Field(
        None, description="List of filter AAAA addresses [IP/Deny|Allow,...]"
    )
    max_cache_ttl: Optional[PositiveInt] = Field(None, description="Max cache TTL in seconds")
    max_ncache_ttl: Optional[PositiveInt] = Field(None, description="Max ncache TTL in seconds")
    rpz_drop_ip_rule_enabled: Optional[bool] = Field(
        None, description="Enable RPZ drop IP rule flag"
    )
    rpz_drop_ip_rule_min_prefix_length_ipv4: Optional[PositiveInt] = Field(
        None, description="RPZ drop IP rule min prefix length IPv4"
    )
    rpz_drop_ip_rule_min_prefix_length_ipv6: Optional[PositiveInt] = Field(
        None, description="RPZ drop IP rule min prefix length IPv6"
    )

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class AuthZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    authzone: str = Field(
        "authzone",
        frozen=True,
        serialization_alias="header-authzone",
        description="CSV header for authzone object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    fqdn: str = Field(..., description="FQDN zone name")
    zone_format: ZoneFormatTypeEnum = Field(..., description="Zone format")
    view: Optional[str] = Field(None, description="View name")
    prefix: Optional[str] = Field(None, description="RFC2317 classless reverse zone Prefix")
    new_prefix: Optional[str] = Field(
        None, serialization_alias="_new_prefix",
        description="New RFC2317 classless reverse zone Prefix"
    )
    is_multimaster: Optional[bool] = Field(None, description="Is multimaster flag")
    grid_primaries: Optional[List[str]] = Field(
        None, description="Grid primary servers [MEMBER/IS_STEALTH,...]"
    )
    external_primaries: Optional[List[str]] = Field(
        None,
        description="External primary servers [FQDN/IP/USE_2X_TSIG/USE_TSIG/NAME/KEY/ALGO,...]"
    )
    grid_secondaries: Optional[List[str]] = Field(
        None,
        description="Grid secondary servers [FQDN/STEALTH/LEAD/GRID_SYNC,...] "
    )
    external_secondaries: Optional[List[str]] = Field(
        None,
        description="External secondary servers [FQDN/IP/USE_2X_TSIG/USE_TSIG/NAME/KEY/ALGO,...]"
    )
    ns_group: Optional[str] = Field(None, description="NS group name")
    comment: Optional[str] = Field(None, description="Optional comment")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    create_underscore_zones: Optional[bool] = Field(
        None, description="Create underscore zones flag"
    )
    allow_active_dir: Optional[List[str]] = Field(
        None, description="List of allowed Active Directory servers"
    )
    soa_refresh: Optional[PositiveInt] = Field(None, description="SOA refresh value")
    soa_retry: Optional[PositiveInt] = Field(None, description="SOA retry value")
    soa_expire: Optional[PositiveInt] = Field(None, description="SOA expire value")
    soa_default_ttl: Optional[PositiveInt] = Field(None, description="SOA default TTL value")
    soa_negative_ttl: Optional[PositiveInt] = Field(None, description="SOA negative TTL value")
    soa_mnames: Optional[List[str]] = Field(
        None,
        description="List of SOA mnames [ZONE/FQDN,...]"
    )
    soa_email: Optional[str] = Field(None, description="SOA email address")
    soa_serial_number: Optional[PositiveInt] = Field(None, description="SOA serial number")
    disable_forwarding: Optional[bool] = Field(
        None, description="Disable forwarding or empty forwarders flag"
    )
    allow_update_forwarding: Optional[bool] = Field(
        None, description="Allow update forwarding flag"
    )
    update_forwarding: Optional[List[str]] = Field(
        None, description="List of update forwarding servers [ITEM/PERMISSION,...]"
    )
    allow_transfer: Optional[List[str]] = Field(
        None, description="List of allowed transfer servers [ITEM/PERMISSION,...]"
    )
    allow_update: Optional[List[str]] = Field(
        None, description="List of allowed update servers [ITEM/PERMISSION,...]"
    )
    allow_query: Optional[List[str]] = Field(
        None, description="List of allowed query servers [ITEM/PERMISSION,...]"
    )
    notify_delay: Optional[PositiveInt] = Field(
        None, ge=5, le=86400, description="Notify delay in seconds")

    @staticmethod
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer(
        'grid_primaries',
        'external_primaries',
        'grid_secondaries',
        'external_secondaries',
        'allow_active_dir',
        'soa_mnames',
        'update_forwarding',
        'allow_transfer',
        'allow_update',
        'allow_query',
    )
    def serialize_list_fields(self, values: Optional[List[str]]) -> Optional[str]:
        return self.list_to_csv(values)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class ForwardZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardzone: str = Field(
        "forwardzone",
        frozen=True,
        serialization_alias="header-forwardzone",
        description="Header for forwardzone object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    fqdn: str = Field(
        ...,
        min_length=1,
        description="FQDN zone name"
    )
    view: Optional[str] = Field(None, description="View name")
    zone_format: ZoneFormatTypeEnum = Field(..., description="Zone format")
    prefix: Optional[str] = Field(None, description="RFC2317 classless reverse zone Prefix")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    comment: Optional[str] = Field(None, description="Optional comment")
    forward_to: Optional[List[str]] = Field(
        None, description="List of forwarders [FQDN/IP,...]"
    )
    forwarding_servers: Optional[List[str]] = Field(
        None, description="List of forwarding servers [FQDN,...]"
    )
    forwarders_only: Optional[bool] = Field(
        True, description="Forwarders only flag"
    )
    ns_group: Optional[str] = Field(None, description="Forwarding Members NS Group")
    ns_group_external: Optional[str] = Field(None, description="Forward-to NS group name")
    disable_ns_generation: Optional[bool] = Field(
        True,
        description="Disable NS generation flag"
    )

    @staticmethod
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer("forward_to", "forwarding_servers", when_used="always")
    def serialize_list_fields(self, values: Optional[List[str]]) -> Optional[str]:
        return self.list_to_csv(values)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class StubZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    stubzone: str = Field(
        "stubzone",
        frozen=True,
        serialization_alias='header-stubzone',
        description='Header for stubzone object'
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    fqdn: str = Field(
        ..., min_length=1, description="FQDN zone name"
    )
    view: Optional[str] = Field(None, description="View name")
    zone_format: ZoneFormatTypeEnum = Field(..., description="Zone format")
    prefix: Optional[PositiveInt] = Field(
        None, description="RFC2317 classless reverse zone Prefix", ge=24, le=32
    )
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    comment: Optional[str] = Field(None, description="Optional comment")
    disable_forwarding: Optional[bool] = Field(None, description="Disable forwarding flag")
    stub_from: Optional[List[str]] = Field(
        None, description="List of stub-from servers [FQDN/IP,...]"
    )
    stub_members: Optional[List[str]] = Field(
        None, description="List of stub-members servers [FQDN,...]"
    )
    ns_group: Optional[str] = Field(None, description="Stub Members NS Group")
    ns_group_external: Optional[str] = Field(None, description="Stub-from NS group name")

    @staticmethod
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer("stub_from", "stub_members", when_used="always")
    def serialize_list_fields(self, values: Optional[List[str]]) -> Optional[str]:
        return self.list_to_csv(values)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    nsgroup: str = Field(
        "nsgroup",
        frozen=True,
        serialization_alias="header-nsgroup",
        description="CSV header for nsgroup object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    group_name: str = Field(..., description="NS group name")
    new_group_name: Optional[str] = Field(
        None, serialization_alias="_new_group_name", description="New NS group name")
    grid_primaries: Optional[List[str]] = Field(
        None, description="Grid primary servers [MEMBER/IS_STEALTH,...]"
    )
    external_primaries: Optional[List[str]] = Field(
        None,
        description="External primary servers [FQDN/IP/STEALTH/USE_2X_TSIG/USE_TSIG/NAME/KEY,...]"
    )
    external_secondaries: Optional[List[str]] = Field(
        None,
        description="External secondary servers [FQDN/IP/STEALTH/USE_2X_TSIG/USE_TSIG/NAME/KEY,...]"
    )
    grid_secondaries: Optional[List[str]] = Field(
        None,
        description="Grid secondary servers [FQDN/IS_STEALTH/LEAD/GRID_SYNC,...] "
    )
    is_grid_default: Optional[bool] = Field(None, description="Is grid default flag")
    comment: Optional[str] = Field(None, description="Optional comment")

    @staticmethod
    def list_to_csv(items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    @field_serializer(
        'grid_primaries',
        'external_primaries',
        'external_secondaries',
        'grid_secondaries',
        when_used="always"
    )
    def serialize_list_fields(self, values: Optional[List[str]]) -> Optional[str]:
        return self.list_to_csv(values)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegatedZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegatedzone: str = Field(
        "delegatedzone",
        frozen=True,
        serialization_alias="header-delegatedzone",
        description="CSV Header for delegatedzone object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    fqdn: str = Field(..., description="FQDN zone name")
    view: Optional[str] = Field(None, description="View name")
    zone_format: ZoneFormatTypeEnum = Field(..., description="Zone format")
    prefix: Optional[PositiveInt] = Field(None, description="RFC2317 classless reverse zone Prefix")
    disabled: Optional[bool] = Field(None, description="Disabled flag")
    comment: Optional[str] = Field(None, description="Optional comment")
    delegate_to: Optional[List[str]] = Field(
        None, description="List of delegated servers [FQDN/IP,...]"
    )
    delegated_ttl: Optional[PositiveInt] = Field(None, description="Delegated TTL")
    ns_group: Optional[str] = Field(None, description="Delegated Members NS Group")
    new_prefix: Optional[PositiveInt] = Field(
        None,
        serialization_alias="_new_prefix",
        description="New RFC2317 classless reverse zone Prefix"
    )
    ddns_protected: Optional[bool] = Field(None, description="DDNS protected flag")
    ddns_principal: Optional[str] = Field(None, description="DDNS principal")

    @field_serializer("delegate_to", when_used="always")
    def serialize_delegate_to(self, items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegationNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegationnsgroup: str = Field(
        "delegationnsgroup",
        frozen=True,
        serialization_alias="header-delegationnsgroup",
        description="Header for delegationnsgroup object")
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action"
    )
    group_name: str = Field(..., description="NS group name")
    new_group_name: Optional[str] = Field(
        None, serialization_alias="_new_group_name", description="New NS group name"
    )
    delegate_to: Optional[List[str]] = Field(
        None, description="List of delegated servers [FQDN/IP,...]"
    )
    comment: Optional[str] = Field(None, description="Optional comment")

    @field_serializer("delegate_to", when_used="always")
    def serialize_delegate_to(self, items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)


class ForwardingMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardingmembernsgroup: str = Field(
        "forwardingmembernsgroup",
        frozen=True,
        serialization_alias="header-forwardingmembernsgroup",
        description="Header for forwardingmembernsgroup object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action")
    group_name: str = Field(..., description="NS group name")
    new_group_name: Optional[str] = Field(
        None, serialization_alias="_new_group_name", description="New NS group name")
    comment: Optional[str] = Field(None, description="Optional comment")
    forwarding_servers: Optional[List[str]] = Field(
        None, description="List of forwarding servers [FQDN/IP,...]"
    )

    @field_serializer("forwarding_servers", when_used="always")
    def serialize_forwarding_servers(self, items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class ForwardStubServerNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardstubservernsgroup: str = Field(
        "forwardstubservernsgroup",
        frozen=True,
        serialization_alias="header-forwardstubservernsgroup",
        description="Header for forwardstubservernsgroup object"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action"
    )
    group_name: str = Field(..., description="NS group name")
    new_group_name: Optional[str] = Field(
        None, serialization_alias="_new_group_name", description="New NS group name")
    comment: Optional[str] = Field(None, description="Optional comment")
    external_servers: Optional[List[str]] = Field(
        None, description="List of external servers [FQDN/IP,...]"
    )

    @field_serializer("external_servers", when_used="always")
    def serialize_external_servers(self, items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class StubMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    stubmembernsgroup: str = Field(
        "stubmembernsgroup",
        frozen=True,
        serialization_alias="header-stubmembernsgroup",
        description="CSV Header for stubmembernsgroup objects"
    )
    import_action: Optional[ImportActionEnum] = Field(
        None, serialization_alias="import-action", description="CSV Custom import action"
    )
    group_name: str = Field(..., description="NS group name", min_length=1)
    new_group_name: Optional[str] = Field(
        None, serialization_alias="_new_group_name", description="New NS group name"
    )
    comment: Optional[str] = Field(None, description="Optional comment")
    stub_members: Optional[List[str]] = Field(
        None, description="List of stub-members servers [FQDN,...]"
    )

    @field_serializer("stub_members", when_used="always")
    def serialize_stub_members(self, items: Optional[List[str]]) -> str | None:
        if not items:
            return None
        return ",".join(items)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")
