# pylint: disable-msg=too-many-arguments
"""
NIOS/CSV Zone Classes
"""
import logging
from collections import defaultdict
from typing import cast, Optional, Any
import dns.query
import dns.tsigkeyring
import dns.zone
from netaddr import IPNetwork, AddrFormatError, NOHOST


class Zone:
    """
    Generic Zone Class w/ common methods
    """

    def __init__(self):
        pass

    @staticmethod
    def zone_from_file(
            filename: str,
            origin: str,
            relativize: bool = False) -> Optional[dns.zone.Zone]:
        """
        return a dns.zone.Zone object from file

        :param filename: string path or filename
        :param origin: zone name
        :param relativize: set to True for relative domain name(s) in the zone

        :raise:
            FileNotFoundError
            dns.zone.NoSOA
            dns.zone.NoNS
            dns.zone.BadZone

        :return: dns.zone.Zone object
        """
        zone = None
        try:
            zone = dns.zone.from_file(
                filename,
                origin=origin,
                relativize=relativize
            )
        except FileNotFoundError as err:
            logging.error(err)
        except dns.zone.NoSOA as err:
            logging.error(err)
        except dns.zone.NoNS as err:
            logging.error(err)
        except dns.zone.BadZone as err:
            logging.error(err)
        return zone

    @staticmethod
    def zone_diff(
            zone1: dns.zone.Zone,
            zone2: dns.zone.Zone,
            ignore_ttl: bool = False,
            ignore_soa: bool = False,
            ignore_ns: bool = False) -> list:
        """
        compare two (2) dns.zone.Zone objects and return list of changes

        The result list will be in the form (name, oldnode, newnode).

        :param zone1: the original DNS zone
        :param zone2: the new DNS zone
        :param ignore_ttl: ignore the TTL differences if true
        :param ignore_soa: ignore differences in the SOA if true
        :param ignore_ns: ignore different NS records if true

        :return list changes:
            the list of differences as changes

        Example::

            # build dns.zone.Zone object for original zone
            orig = dns.zone.from_file(
                orig_zonefile,
                zone_name,
                relativize=False
            )

            # build dns.zone.Zone object for new/current zone
            new = dns.zone.from_file(
                new_zonefile,
                zone_name,
                relativize=False
            )

            # perform zone comparison
            zone_differences = Zone.zone_diff(
                zone1=orig,
                zone2=new,
                ignore_ttl=ignore_ttl,
                ignore_soa=ignore_soa,
                ignore_ns=ignore_ns
            )

        """
        origin = zone1.origin
        logging.debug('origin = %s', origin)
        changes = []
        for name in zone1:
            name_str = str(name)
            node1 = cast(dns.node.Node, zone1.get_node(name_str))
            node2 = cast(dns.node.Node, zone2.get_node(name_str))
            if not node2:
                changes.append((str(name), node1, node2))
                logging.debug((str(name), node1, node2))
            elif Zone._nodes_differ(
                    node1,
                    node2,
                    ignore_ttl):
                changes.append((str(name), node1, node2))
                logging.debug((str(name), node1, node2))

        for name in zone2:
            node3 = cast(dns.node.Node, zone1.get_node(name))
            if not node3:
                node4 = cast(dns.node.Node, zone2.get_node(name))
                changes.append((str(name), node3, node4))
                logging.debug((str(name), node3, node4))

        filtered_changes = Zone._zone_diff_filter(
            origin=origin,
            changes=changes,
            ignore_ttl=ignore_ttl,
            ignore_soa=ignore_soa,
            ignore_ns=ignore_ns
        )
        return filtered_changes

    @staticmethod
    def _nodes_differ(
            node1: dns.node.Node,
            node2: dns.node.Node,
            ignore_ttl: bool) -> bool:
        """
        perform comparison of two (2) dns.node.Node objects w/ common name

        :param node1: original DNS node object
        :param node2: new DNS node object
        :param ignore_ttl: ignore TTL differences if true

        :return bool: True if the nodes differ
        """
        if not ignore_ttl:
            for rd_set in node1.rdatasets:
                if rd_set not in node2.rdatasets:
                    return True
                if not ignore_ttl:
                    return rd_set.ttl != node2.find_rdataset(
                        rd_set.rdclass,
                        rd_set.rdtype).ttl

            for rd_set in node2.rdatasets:
                if rd_set not in node1.rdatasets:
                    return True
            return False

        return node1 != node2

    @staticmethod
    def _zone_diff_filter(
            origin: str,
            changes: list,
            ignore_ttl: bool = False,
            ignore_soa: bool = False,
            ignore_ns: bool = False) -> list:
        """
        filter the zone diff changes

        :param origin: zone origin used for delegation check(s)
        :param changes: list of zone differences
        :param ignore_ttl: set to `True` to ignore TTL differences in records
        :param ignore_soa: set to `True` to ignore SOA differences in zones
        :param ignore_ns: set to `True` to ignore NS record differences in zones

        :return list: filtered result list of zone changes
        """
        res = []
        for name, old, new in changes:
            if not old:
                for rd_set in new.rdatasets:
                    rclass = dns.rdataclass.to_text(rd_set.rdclass)
                    rtype = dns.rdatatype.to_text(rd_set.rdtype)
                    ttl = rd_set.ttl
                    if ignore_soa and rtype == 'SOA':
                        continue
                    if (
                            ignore_ns and
                            rtype == 'NS' and
                            dns.name.from_text(name) == origin
                    ):
                        continue
                    for r_data in rd_set:
                        res.append(('++', name, ttl, rclass, rtype, r_data))
            elif not new:
                for rd_set in old.rdatasets:
                    rclass = dns.rdataclass.to_text(rd_set.rdclass)
                    rtype = dns.rdatatype.to_text(rd_set.rdtype)
                    ttl = rd_set.ttl
                    if ignore_soa and rtype == 'SOA':
                        continue
                    if (
                            ignore_ns and
                            rtype == 'NS' and
                            dns.name.from_text(name) == origin
                    ):
                        continue
                    for r_data in rd_set:
                        res.append(('--', name, ttl, rclass, rtype, r_data))
            else:
                for rd_set in old.rdatasets:
                    rclass = dns.rdataclass.to_text(rd_set.rdclass)
                    rtype = dns.rdatatype.to_text(rd_set.rdtype)
                    ttl = rd_set.ttl
                    if ignore_soa and rtype == 'SOA':
                        continue
                    if (
                            ignore_ns and
                            rtype == 'NS' and
                            dns.name.from_text(name) == origin
                    ):
                        continue
                    if rd_set not in new.rdatasets or (
                            rd_set.ttl != new.find_rdataset(rd_set.rdclass, rd_set.rdtype).ttl
                            and not ignore_ttl
                    ):
                        for r_data in rd_set:
                            res.append(('~-', name, ttl, rclass, rtype, r_data))
                for rd_set in new.rdatasets:
                    rclass = dns.rdataclass.to_text(rd_set.rdclass)
                    rtype = dns.rdatatype.to_text(rd_set.rdtype)
                    ttl = rd_set.ttl
                    if ignore_soa and rtype == 'SOA':
                        continue
                    if (
                            ignore_ns and
                            rtype == 'NS' and
                            dns.name.from_text(name) == origin
                    ):
                        continue
                    if rd_set not in old.rdatasets or (
                            rd_set.ttl != old.find_rdataset(rd_set.rdclass, rd_set.rdtype).ttl
                            and not ignore_ttl
                    ):
                        for r_data in rd_set:
                            res.append(('~+', name, ttl, rclass, rtype, r_data))
        return res

    @staticmethod
    def get_zone_from_addr(network: str) -> str:
        """
        convert network address to reverse domain name

        :param network: IP network address
        :return str:
            string value of the domain name
        """
        reverse_zone = ''
        if '/' in network:
            addr, cidr = network.split('/', 2)
            octets = addr.split('.')
            if cidr == '8':
                reverse_zone = f'{octets[0]}.in-addr.arpa'
            elif cidr == '16':
                reverse_zone = f'{octets[1]}.{octets[0]}.in-addr.arpa'
            elif cidr == '24':
                reverse_zone = f'{octets[2]}.{octets[1]}.{octets[0]}.in-addr.arpa'
            else:
                logging.warning(
                    'unable to parse %s into reverse dns zone name', network
                )
        return reverse_zone

    @staticmethod
    def get_zone_prefix(origin: str) -> str:
        """
        get prefix for RFC2317 reverse zone(s)

        There are two (2) formats for RFC2317:

        0/25.1.168.192.in-addr.arpa
        0-25.1.168.192.in-addr.arpa

        :param origin: domain name
        :return str:
            string value of the prefix if RFC2317 or empty string
        """
        prefix = ''
        if 'in-addr.arpa' in origin:
            addr = origin.replace('.in-addr.arpa', '')
            octets = addr.split('.')
            if '-' in addr or '/' in addr:
                prefix = octets[0]
        return prefix

    @staticmethod
    def get_zone_type(zone_name: str) -> str:
        """
        calculate the Infoblox zone type from zone name

        :param zone_name: DNS zone name
        :return str:
            Infoblox zone type FORWARD | IPV4 | IPV6
        """
        if 'in-addr.arpa' in zone_name.lower():
            zone_type = 'IPV4'
        elif 'ip6.arpa' in zone_name.lower():
            zone_type = 'IPV6'
        else:
            zone_type = 'FORWARD'
        return zone_type

    @staticmethod
    def get_rev_zone_addr(origin: str) -> str:
        """
        convert reverse zone to x.x.x.x/y format for Infoblox CSV import

        :param origin: DNS zone name
        :return str:
            a string representation of a network address
        """
        cidrs = {
            256: 24,
            128: 25,
            64: 26,
            32: 27,
            16: 28,
            8: 29,
            4: 30,
            2: 31,
            1: 32
        }
        zone_address = ''
        if 'in-addr.arpa' in origin:
            addr = origin.replace('.in-addr.arpa', '')
            octets = addr.split('.')
            octets.reverse()
            if len(octets) == 1:
                zone_address = f'{octets[0]}.0.0.0/8'
            elif len(octets) == 2:
                zone_address = f'{octets[0]}.{octets[1]}.0.0/16'
            elif len(octets) == 3:
                zone_address = f'{octets[0]}.{octets[1]}.{octets[2]}.0/24'
            elif len(octets) == 4:
                if '/' in octets[3]:
                    last, cidr = octets[3].split('/')
                    _address = f'{octets[0]}.{octets[1]}.{octets[2]}.{last}/{cidr}'
                elif '-' in octets[3]:
                    start, end = octets[3].split('-')
                    hosts = abs(int(start) - int(end)) + 1
                    _address = f'{octets[0]}.{octets[1]}.{octets[2]}.{start}/{cidrs.get(hosts)}'
                else:
                    logging.error('error parsing reverse zone %s', origin)
                    raise ValueError
                try:
                    zone_address = IPNetwork(_address, flags=NOHOST)
                except AddrFormatError as err:
                    logging.error(err)
                    raise AddrFormatError
            else:
                logging.error('error parsing reverse zone %s', origin)
        elif 'ip6.arpa' in origin:
            addr = origin.replace('.ip6.arpa', '')
            octets = addr.split('.')
            octets.reverse()
            cidr = len(octets) * 4
            ipv6_str = ''.join(octet for octet in octets)
            while len(ipv6_str) % 4 != 0:
                ipv6_str += '0'
            ipv6_addr = ':'.join(ipv6_str[i:i+4] for i in range(0, len(ipv6_str), 4))
            try:
                zone_address = IPNetwork(f'{ipv6_addr}::/{cidr}')
            except AddrFormatError as err:
                logging.error(err)
        else:
            try:
                zone_address = IPNetwork(origin)
            except AddrFormatError as err:
                logging.error(err)
        return str(zone_address)

    @staticmethod
    def zone_transfer(
            zone_name: str,
            nameserver: str,
            keyring: Optional[Any] = None,
            relativize: Optional[bool] = False,
            timeout: Optional[int] = 5,
            lifetime: Optional[int] = 15):
        """
        perform a DNS zone transfer or AXFR query to a nameserver

        This method will perform a DNS zone AXFR or zone transfer from the
        provided nameserver. This method accepts a tsig keyring object from
        the DNS python package. Ordinarily, this method should always set
        ``relativize`` to False so that everything is fully-qualified and
        normalized.

        :param zone_name: name of the zone to transfer
        :param nameserver: IP address of the name server
        :param keyring: (Optional) TSIG keyring object
        :param relativize: (Optional) relative if true, else fully-qualified
            when false
        :param timeout: (Optional) the max # of seconds to wait between response
            packets
        :param lifetime: (Optional) the max # of seconds to wait for the entire
            xfer

        :raises:
            dns.exception.Timeout
            dns.exception.DNSException

        :return:
            dns.zone.Zone object
        """

        if not zone_name.endswith('.'):
            zone_name += '.'

        zone = dns.zone.Zone(zone_name, relativize=relativize)

        axfr_query, dummy = dns.xfr.make_query(
            zone, keyring=keyring
        )
        try:
            dns.query.inbound_xfr(
                nameserver,
                zone,
                query=axfr_query,
                timeout=timeout,
                lifetime=lifetime
            )
        except dns.exception.Timeout as err:
            logging.error(
                'dns axfr timed out for %s from %s', zone_name, nameserver
            )
            raise err
        except dns.exception.DNSException as err:
            logging.error(
                'dns axfr exception for %s from %s',
                zone_name, nameserver
            )
            raise err
        else:
            return zone


class AuthZone(Zone):
    """
    Authoritative DNS Zone object/class
    """
    DEFAULT_OBJECT = {
        'header-authzone': 'authzone',
        'fqdn': '',
        'zone_format': '',
        'prefix': '',
        'view': '',
        'disable_forwarding': '',
        'ns_group': '',
        'soa_serial_number': '',
        'soa_mnames': '',
        'soa_email': '',
        'soa_refresh': '',
        'soa_retry': '',
        'soa_expire': '',
        'soa_negative_ttl': '',
        'soa_default_ttl': '',
    }

    def __init__(
            self,
            authzone: dns.zone.Zone,
            dns_view: str = '',
            ns_group: str = '',
            soa_from_zone: bool = False,
            soa_serial_increase: int = 1000000):
        # get the origin as string non-dot-terminated
        super().__init__()
        origin = str(authzone.origin).rstrip('.')

        # get the zone format FORWARD, IPV4 or IPV6
        zone_format = self.get_zone_type(origin)

        # pull out the SOA record for setting zone timers
        soa = authzone.get_rdataset(authzone.origin, dns.rdatatype.SOA, create=False)
        if isinstance(soa, dns.rdataset.Rdataset):
            soa_current_serial = int(soa[0].serial)
            logging.debug(soa)
        else:
            soa_current_serial = 0

        # calculate the new serial current_serial + serial_increase
        new_serial_number = self.increment_serial_num(
            soa_current_serial,
            soa_serial_increase
        )

        # file the object w/ defaults
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)

        self.fqdn = origin
        self.zone_format = zone_format
        self.view = dns_view
        self.disable_forwarding = True
        self.ns_group = ns_group
        self.soa_serial_number = new_serial_number
        self.soa_mnames = ''

        if soa_from_zone:
            self.soa_email = self.rname_to_email(soa[0].rname)
            self.soa_refresh = soa[0].refresh
            self.soa_retry = soa[0].retry
            self.soa_expire = soa[0].expire
            self.soa_negative_ttl = soa[0].minimum
            self.soa_default_ttl = soa.ttl

        if zone_format == 'IPV4':
            self.fqdn = self.get_rev_zone_addr(origin)
            self.prefix = self.get_zone_prefix(origin)

        logging.debug(self.__dict__)
        # keys = list(self.cols())
        # keys.insert(1, 'IMPORT-ACTION')
        # logging.debug(keys)

    @staticmethod
    def cols():
        """
        return list of CSV column names
        :return: list of column names
        """
        return list(AuthZone.DEFAULT_OBJECT.keys())

    @staticmethod
    def rname_to_email(rname: dns.name.Name) -> str:
        """
        convert dns.name.Name object to Infoblox SOA Email format

        :param dns.name.Name rname: The rname field of the SOA
        :return: converted string valueof the email address
        """
        hostname = str(rname).rstrip('.')
        return hostname.replace('.', '@', 1)

    @staticmethod
    def increment_serial_num(
            cur_serial: int,
            soa_serial_increase) -> int:
        """
        calculate new SOA serial number

        :param int cur_serial: current value of the serial number
        :param int soa_serial_increase: SOA serial increment value
        :return:
            incremented DNS SOA serial number
        """
        return (cur_serial + soa_serial_increase) % 2 ** 32

    @staticmethod
    def get_delegated_zones(
            zone_object: dns.zone.Zone,
            view: str,
            zone_list: list) -> list:
        """
        extract zone delegation(s) from zone

        :param dns.zone.Zone zone_object: DNS zone object from dnspython
        :param str view: DNS view name
        :param list zone_list: list of zone(s) to check against
        :return list: list of Infoblox CSV delegatedzone object(s)
        """
        delegations = defaultdict(list)
        delegated_zones = []
        parent_zone = str(zone_object.origin).rstrip('.')

        # process the NS records for delegation(s)
        for rdatas in zone_object.iterate_rdatas('NS'):
            zone_name = str(rdatas[0]).rstrip('.').lower()
            nameserver = str(rdatas[2].target).rstrip('.')

            if zone_name != parent_zone and zone_name not in zone_list:
                delegations[zone_name].append(nameserver)

        for delegation, value in delegations.items():
            delegate_to = []
            servers = value
            for server in servers:
                nameserver = f'{server}/255.255.255.255'
                delegate_to.append(nameserver)

            delegated_zone = DelegatedZone(
                fqdn=delegation,
                view=view,
                zone_format=Zone.get_zone_type(delegation),
                delegate_to=','.join(delegate_to)
            )
            delegated_zones.append(delegated_zone)

        return delegated_zones


class DelegatedZone(Zone):
    """
    Zone Delegation or delegatedzone NIOS / CSV object class
    """
    DEFAULT_OBJECT = {
        'header-delegatedzone': 'delegatedzone',
        'fqdn': '',
        'prefix': '',
        'view': '',
        'zone_format': '',
        'delegate_to': ''
    }

    def __init__(self,
                 fqdn: str,
                 view: str,
                 zone_format: str,
                 delegate_to: str):
        super().__init__()
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)

        self.fqdn = fqdn
        self.view = view
        self.zone_format = zone_format
        self.delegate_to = delegate_to

        if zone_format == 'IPV4':
            self.fqdn = self.get_rev_zone_addr(fqdn)
            self.prefix = self.get_zone_prefix(fqdn)

        logging.debug(self.__dict__)

    @staticmethod
    def cols():
        """
        return list of CSV column names for the header
        :return: list of CSV column name(s)
        """
        return list(DelegatedZone.DEFAULT_OBJECT.keys())


class ForwardZone(Zone):
    """
    Conditional Forward Zone or forwardzone NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-forwardzone': 'forwardzone',
        'fqdn': '',
        'view': '',
        'zone_format': '',
        'prefix': '',
        'forward_to': '',
        'forwarding_servers': '',
        'forwarders_only': '',
        'ns_group': '',
        'ns_group_external': '',
        'disable_ns_generation': False
    }

    def __init__(self,
                 fqdn: str,
                 view: str = '',
                 forward_to: str = '',
                 forwarders_only: bool = True,
                 ns_group: str = '',
                 ns_group_external: str = ''):
        super().__init__()
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)

        self.fqdn = fqdn
        self.view = view
        self.zone_format = Zone.get_zone_type(fqdn)
        self.forward_to = forward_to
        self.forwarders_only = forwarders_only
        self.ns_group = ns_group
        self.ns_group_external = ns_group_external
        logging.debug(self.__dict__)

    def disable_ns_generation(self):
        """
        set disable_ns_generation to True
        :return None:
        """
        setattr(self, 'disable_ns_generation', True)

    @staticmethod
    def cols():
        """
        return list of CSV column name(s)
        :return: list of CSV column names
        """
        return list(ForwardZone.DEFAULT_OBJECT.keys())
