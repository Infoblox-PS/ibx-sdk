from .enums import ZoneFormatTypeEnum, ImportActionEnum

from pydantic import BaseModel, Field, ConfigDict, PositiveInt


class MemberDns(BaseModel):
    model_config = ConfigDict(extra="allow")

    memberdns: str = Field(alias="header-memberdns", default="memberdns")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    parent: str
    dns_over_mgmt: bool | None = None
    dns_over_lan2: bool | None = None
    minimal_response: bool | None = None
    forwarders_only: bool | None = None
    allow_forwarder: str | None = None  # list of ip addresses
    member_view_nats: str | None = None  # example: external_dns/INTERFACE/10.10.10.10
    enable_notify_source_port: bool | None = None
    notify_source_port: PositiveInt | None = None
    enable_query_source_port: bool | None = None
    query_source_port: PositiveInt | None = None
    lame_ttl: PositiveInt | None = None
    auto_sort_views: bool | None = None
    member_views: str | None = None
    allow_transfer: str | None = None  # Example: NACL1 or "12.0.0.12/Deny,1234::/64/Allow"
    excluded_servers: str | None = None
    zone_transfer_format_option: str | None = None
    recursion_enabled: bool | None = None
    allow_query: str | None = None  # ACL
    allow_recursive_query: str | None = None  # ACL
    limit_concurrent_recursive_clients: bool | None = None
    concurrent_recursive_clients: PositiveInt | None = Field(default=1000)
    allow_update: str | None = None
    allow_gss_tsig_zone_updates: bool | None = None
    allow_update_forwarding: bool | None = None
    enable_custom_root_server: bool | None = None
    root_name_servers: str | None = None
    enable_blackhole: bool | None = None
    blackhole: str | None = None  # ACL
    notify_delay: PositiveInt | None = Field(ge=5, le=86400)
    enable_nxdomain_redirect: bool | None = None
    nxdomain_redirect_addresses: str | None = None
    nxdomain_redirect_ttl: PositiveInt | None = None
    nxdomain_log_query: bool | None = None
    nxdomain_rulesets: str | None = None
    enable_blacklist: bool | None = None
    blacklist_redirect_addresses: str | None = None
    blacklist_action: str | None = None
    blacklist_redirect_ttl: PositiveInt | None = None
    blacklist_log_query: bool | None = None
    blacklist_rulesets: str | None = None
    enable_dns64: bool | None = None
    dns64_groups: str | None = None
    max_cached_lifetime: PositiveInt | None = Field(ge=60, le=86400, default=86400)
    dns_over_v6_mgmt: bool | None = None
    dns_over_v6_lan2: bool | None = None
    filter_aaaa: str | None = None
    filter_aaaa_list: str | None = None
    dns_over_v6_lan: bool | None = None
    copy_xfer_to_notify: bool | None = None
    transfers_in: PositiveInt | None = Field(ge=10, le=100, default=10)
    transfers_out: PositiveInt | None = Field(ge=10, le=100, default=10)
    transfers_per_ns: PositiveInt | None = Field(ge=2, le=100)
    serial_query_rate: PositiveInt | None = Field(ge=20, le=100, default=20)
    max_cache_ttl: PositiveInt | None = Field(default=86400)
    max_ncache_ttl: PositiveInt | None = Field(le=604800, default=10800)
    disable_edns: bool | None = None
    query_rewrite_enabled: bool | None = None
    rpz_drop_ip_rule_enabled: bool | None = None
    rpz_drop_ip_rule_min_prefix_length_ipv4: PositiveInt | None = Field(ge=0, le=32, default=29)
    rpz_drop_ip_rule_min_prefix_length_ipv6: PositiveInt | None = Field(ge=0, le=128, default=112)
    atc_forwarding_enable: bool | None = None
    atc_forwarding_access_key: str | None = None
    atc_forwarding_resolver_address: str | None = None
    atc_forwarding_forward_first: bool | None = None


class AuthZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    authzone: str = Field(alias="header-authzone", default="authzone")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    zone_format: ZoneFormatTypeEnum
    view: str | None = None
    prefix: str | None = None
    new_prefix: str | None = Field(alias="_new_prefix", default=None)
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

    forwardzone: str = Field(alias="header-forwardzone", default="forwardzone")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
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

    stubzone: str = Field(alias='header-stubzone', default='stubzone')
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    view: str | None = None
    zone_format: ZoneFormatTypeEnum
    prefix: str | None = None
    disabled: bool | None = None
    comment: str | None = None
    disable_forwarding: bool | None = None
    stub_from: str | None = None # list of [<fqdn>/<ip>,...]
    stub_members: str | None = None # list of Grid members
    ns_group: str | None = None
    ns_group_external: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class NsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    nsgroup: str = Field(alias="header-nsgroup", default="nsgroup")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    group_name: str
    new_group_name: str | None = Field(alias="_new_group_name", default=None)
    grid_primaries: str | None = None # list of <fqdn>/<stealth_flag>
    external_primaries: str | None = None # list of <fqdn>/<ip>/<use_2x_tsig>/<use_tsig>/<name>/<key>
    external_secondaries: str | None = None # list of name/ip/use_2x_tsig/use_tsig/name/key
    grid_secondaries: str | None = None # list of fqdn/stealth/lead/grid_sync
    is_grid_default: bool | None = None
    comment: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegatedZone(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegatedzone: str = Field(alias="header-delegatedzone", default="delegatedzone")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    fqdn: str
    view: str | None = None
    zone_format: ZoneFormatTypeEnum
    prefix: str | None = None
    disabled: bool | None = None
    comment: str | None = None
    delegate_to: str | None = None  # list of <fqdn>/<ip>
    delegated_ttl: PositiveInt | None = None
    ns_group: str | None = None
    new_prefix: str | None = Field(alias="_new_prefix", default=None)
    ddns_protected: bool | None = None
    ddns_principal: str | None = None

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-") or prop.startswith("ADMGRP-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class DelegationNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    delegationnsgroup: str = Field(alias="header-delegationnsgroup", default="delegationnsgroup")
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    group_name: str
    new_group_name: str | None = Field(alias="_new_group_name", default=None)
    delegate_to: str  # list of <fqdn>/<ip> servers
    comment: str | None = None


class ForwardingMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardingmembernsgroup: str = Field(
        alias="header-forwardingmembernsgroup", default="forwardingmembernsgroup"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    group_name: str
    new_group_name: str | None = Field(alias="_new_group_name", default=None)
    comment: str | None = None
    forwarding_servers: str # list of use_forwarders/override_default_fwds/grid_member/[fqdn/ip]

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class ForwardStubServerNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    forwardstubservernsgroup: str = Field(
            alias="header-forwardstubservernsgroup", default="forwardstubservernsgroup"
        )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    group_name: str
    new_group_name: str | None = Field(alias="_new_group_name", default=None)
    comment: str | None = None
    external_servers: str # list of external servers

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")


class StubMemberNsGroup(BaseModel):
    model_config = ConfigDict(extra="allow")

    stubmembernsgroup: str = Field(
        alias="header-stubmembernsgroup", default="stubmembernsgroup"
    )
    import_action: ImportActionEnum | None = Field(alias="import-action", default=None)
    group_name: str
    new_group_name: str | None = Field(alias="_new_group_name", default=None)
    comment: str | None = None
    stub_members: str # list of grid members

    def add_property(self, prop: str, value: str):
        if prop.startswith("EA-"):
            self.__setattr__(prop, value)
        else:
            raise Exception(f"Invalid field name: {prop}")



