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

class AuthZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    authzone: str = Field(serialization_alias="header-authzone", default="authzone")
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    fqdn: str
    zone_format: ZoneFormatTypeEnum
    view: str | None = None
    prefix: str | None = None
    new_prefix: str | None = Field(serialization_alias="_new_prefix", default=None)
    is_multimaster: bool | None = None
    grid_primaries: str | None = None  # list of FQDN/IS_STEALTH flag
    external_primaries: str | None = None  # Example: "ext1.test.com/1.1.1.1/FALSE"
    grid_secondaries: str | None = None  # Data must be in the following format: "hostname/stealth/lead/grid_ replicate"
    external_secondaries: str | None = None
    ns_group: str | None = None
    comment: str | None = None
    disabled: bool | None = None
    create_underscore_zones: bool | None = None
    allow_active_dir: str | None = None  # List of allowed IPs of DCs
    soa_refresh: PositiveInt | None = None
    soa_retry: PositiveInt | None = None
    soa_expire: PositiveInt | None = None
    soa_default_ttl: PositiveInt | None = None
    soa_negative_ttl: PositiveInt | None = None
    soa_mnames: str | None = None
    soa_email: str | None = None
    soa_serial_number: PositiveInt | None = None
    disable_forwarding: bool | None = None  # Do not use forwarders
    allow_update_forwarding: bool | None = None
    update_forwarding: str | None = None  # ACL
    allow_transfer: str | None = None  # ACL
    allow_update: str | None = None  # ACL
    allow_query: str | None = None  # ACL
    notify_delay: PositiveInt | None = Field(ge=5, le=86400)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class ForwardZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardzone: str = Field(serialization_alias="header-forwardzone", default="forwardzone")
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    fqdn: str
    view: str | None = None
    zone_format: ZoneFormatTypeEnum
    prefix: str | None = None
    disabled: bool | None = None
    comment: str | None = None
    forward_to: str | None = None  # list of forwarders "fqdn/ip,fqdn2/ip"
    forwarding_servers: str | None = None  # list of fqdns of Grid Members
    forwarders_only: bool | None = Field(default=True)
    ns_group: str | None = None
    ns_group_external: str | None = None
    disable_ns_generation: bool | None = Field(default=True)

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class StubZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    stubzone: str = Field(serialization_alias='header-stubzone', default='stubzone')
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    fqdn: str
    view: str | None = None
    zone_format: ZoneFormatTypeEnum
    prefix: str | None = None
    disabled: bool | None = None
    comment: str | None = None
    disable_forwarding: bool | None = None
    stub_from: str | None = None  # list of [<fqdn>/<ip>,...]
    stub_members: str | None = None  # list of Grid members
    ns_group: str | None = None
    ns_group_external: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    nsgroup: str = Field(serialization_alias="header-nsgroup", default="nsgroup")
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    group_name: str
    new_group_name: str | None = Field(serialization_alias="_new_group_name", default=None)
    grid_primaries: str | None = None  # list of <fqdn>/<stealth_flag>
    external_primaries: str | None = None  # list of <fqdn>/<ip>/<use_2x_tsig>/<use_tsig>/<name>/<key>
    external_secondaries: str | None = None  # list of name/ip/use_2x_tsig/use_tsig/name/key
    grid_secondaries: str | None = None  # list of fqdn/stealth/lead/grid_sync
    is_grid_default: bool | None = None
    comment: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegatedZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegatedzone: str = Field(serialization_alias="header-delegatedzone", default="delegatedzone")
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    fqdn: str
    view: str | None = None
    zone_format: ZoneFormatTypeEnum
    prefix: str | None = None
    disabled: bool | None = None
    comment: str | None = None
    delegate_to: str | None = None  # list of <fqdn>/<ip>
    delegated_ttl: PositiveInt | None = None
    ns_group: str | None = None
    new_prefix: str | None = Field(serialization_alias="_new_prefix", default=None)
    ddns_protected: bool | None = None
    ddns_principal: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegationNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegationnsgroup: str = Field(serialization_alias="header-delegationnsgroup",
                                   default="delegationnsgroup")
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    group_name: str
    new_group_name: str | None = Field(serialization_alias="_new_group_name", default=None)
    delegate_to: str  # list of <fqdn>/<ip> servers
    comment: str | None = None


class ForwardingMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardingmembernsgroup: str = Field(
        serialization_alias="header-forwardingmembernsgroup", default="forwardingmembernsgroup"
    )
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    group_name: str
    new_group_name: str | None = Field(serialization_alias="_new_group_name", default=None)
    comment: str | None = None
    forwarding_servers: str  # list of use_forwarders/override_default_fwds/grid_member/[fqdn/ip]

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class ForwardStubServerNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardstubservernsgroup: str = Field(
        serialization_alias="header-forwardstubservernsgroup", default="forwardstubservernsgroup"
    )
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    group_name: str
    new_group_name: str | None = Field(serialization_alias="_new_group_name", default=None)
    comment: str | None = None
    external_servers: str  # list of external servers

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class StubMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    stubmembernsgroup: str = Field(
        serialization_alias="header-stubmembernsgroup", default="stubmembernsgroup"
    )
    import_action: ImportActionEnum | None = Field(serialization_alias="import-action",
                                                   default=None)
    group_name: str
    new_group_name: str | None = Field(serialization_alias="_new_group_name", default=None)
    comment: str | None = None
    stub_members: str  # list of grid members

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")
