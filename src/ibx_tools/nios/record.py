# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
"""
Infoblox DNS/CSV/NIOS objects

"""
import csv
from typing import List, Optional, Union
import logging
import pprint
from collections import defaultdict

import dns.name
import dns.reversename

logging.getLogger(__file__)


class Record:
    """
    DNS Record - common methods to all DNS Record types
    """

    @staticmethod
    def hash_of_records_by_name(list_of_recs, obj_type):
        """
        return a hash of records by fqdn

        :param list_of_recs: list of NIOS/CSV object(s)
        :param obj_type: string value of the object type to hash on

        :return: dictionary of records hashed on fqdn
        """
        hash_of_recs = defaultdict(list)
        for rec in list_of_recs:
            if obj_type in ['arecord', 'aaaarecord']:
                hash_of_recs[rec.fqdn].append(rec)
            elif obj_type in ['ptrrecord']:
                hash_of_recs[rec.dname].append(rec)
        return hash_of_recs

    @staticmethod
    def matching_fqdns(hash1, hash2):
        """
        find matching FQDNs from two (2) hashes

        :param hash1: primary hash
        :param hash2: secondary hash to compare to primary

        :return: list of matching names from two (2) hashes
        """
        return [fqdn for fqdn in hash1 if fqdn in hash2]


class HostRecord:
    """
    Host Record Class
    """
    DEFAULT_OBJECT = {
        'header-hostrecord': 'hostrecord',
        'fqdn': '',
        'addresses': '',
        'ipv6_addresses': '',
        'view': '',
        'ttl': ''
    }
    all_host_records: List['HostRecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 addresses: str,
                 ipv6_addresses: str,
                 view: Optional[str] = None,
                 ttl: Optional[int] = None
                 ):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.addresses = addresses
        self.ipv6_addresses = ipv6_addresses
        HostRecord.all_host_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns

        :return: list of column headers
        """
        return list(HostRecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'hostrecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_host_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column
        :return: count of hostrecord objects written to file
        """
        if HostRecord.all_host_records:
            cols = HostRecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in HostRecord.all_host_records:
                    mywriter.writerow(row.__dict__)
        return len(HostRecord.all_host_records)


class ARecord:
    """
    A Record or arecord object class
    """
    DEFAULT_OBJECT = {
        'header-arecord': 'arecord',
        'fqdn': '',
        'address': '',
        'view': '',
        'ttl': '',
    }
    all_a_records: List['ARecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 address: str,
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.address = address
        ARecord.all_a_records.append(self)

    def __hash__(self):
        return hash((
            self.fqdn,
            self.address,
            self.view
        ))

    def ea(self, prop: str, value: str):
        """
        Create EA fields and add to the object

        :param prop: EA field name
        :param value: EA value
        :return:
            None
        """
        setattr(self, f'EA-{prop}', value)

    def __matching__(self, ptr):
        return hash((
            self.fqdn, self.address, self.view
        )) == hash((
            ptr.dname, ptr.ip, ptr.view
        ))

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(ARecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'arecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_a_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: count of arecord objects written to file
        """
        if ARecord.all_a_records:
            cols = ARecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in ARecord.all_a_records:
                    mywriter.writerow(row.__dict__)
        return len(ARecord.all_a_records)


class AAAARecord:
    """
    AAAA record or aaaarecord NIOS/CSV object
    """
    DEFAULT_OBJECT = {
        'header-aaaarecord': 'aaaarecord',
        'fqdn': '',
        'address': '',
        'view': '',
        'ttl': '',
    }
    all_aaaa_records: List['AAAARecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 address: str,
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.address = address
        AAAARecord.all_aaaa_records.append(self)

    def __hash__(self):
        return hash((
            self.fqdn,
            self.address,
            self.view
        ))

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(AAAARecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'aaaarecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_aaaa_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: count of AAAA records written to file
        """
        if AAAARecord.all_aaaa_records:
            cols = AAAARecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in AAAARecord.all_aaaa_records:
                    mywriter.writerow(row.__dict__)
        return len(AAAARecord.all_aaaa_records)


class CAARecord:
    """
    CAA record or caarecord Infoblox NIOS/CSV object
    """
    DEFAULT_OBJECT = {
        'header-caarecord': 'caarecord',
        'fqdn': '',
        'ca_flag': '',
        'ca_tag': '',
        'ca_value': '',
        'view': '',
        'ttl': ''
    }
    all_caa_records: List['CAARecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 ca_flag: Union[str, int],
                 ca_tag: Union[str, bytes],
                 ca_value: Union[str, bytes],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.ca_flag = ca_flag
        if isinstance(ca_tag, bytes):
            self.ca_tag = ca_tag.decode('utf8')
        else:
            self.ca_tag = ca_tag
        if isinstance(ca_value, bytes):
            self.ca_value = ca_value.decode('utf8')
        else:
            self.ca_value = ca_value
        self.view = view
        self.ttl = ttl
        CAARecord.all_caa_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(CAARecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'caarecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_caa_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: count of caarecord objects written to file
        """
        if CAARecord.all_caa_records:
            cols = CAARecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in CAARecord.all_caa_records:
                    mywriter.writerow(row.__dict__)
        return len(CAARecord.all_caa_records)


class CNAMERecord:
    """
    CNAME record or cnamerecord NIOS/CSV object
    """
    DEFAULT_OBJECT = {
        'header-cnamerecord': 'cnamerecord',
        'fqdn': '',
        'canonical_name': '',
        'view': '',
        'ttl': '',
    }
    all_cname_records: List['CNAMERecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 canonical_name: Union[str, dns.name.Name],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.canonical_name = str(canonical_name).rstrip('.')
        CNAMERecord.all_cname_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(CNAMERecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'cnamerecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_cname_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of cnamerecord objects written to file
        """
        if CNAMERecord.all_cname_records:
            cols = CNAMERecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in CNAMERecord.all_cname_records:
                    mywriter.writerow(row.__dict__)
        return len(CNAMERecord.all_cname_records)


class DNAMERecord:
    """
    DNAME Record or dnamerecord NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-dnamerecord': 'dnamerecord',
        'fqdn': '',
        'target': '',
        'view': '',
        'ttl': '',
    }
    all_dname_records: List['DNAMERecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 target: Union[str, dns.name.Name],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.target = str(target).rstrip('.')
        DNAMERecord.all_dname_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(DNAMERecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'dnamerecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_dname_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of dnamerecord objects written to file
        """
        if DNAMERecord.all_dname_records:
            cols = DNAMERecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in DNAMERecord.all_dname_records:
                    mywriter.writerow(row.__dict__)
        return len(DNAMERecord.all_dname_records)


class MXRecord:
    """
    MX Record or mxrecord NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-mxrecord': 'mxrecord',
        'fqdn': '',
        'priority': '',
        'mx': '',
        'view': '',
        'ttl': '',
    }
    all_mx_records: List['MXRecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 priority: str,
                 mx: Union[str, dns.name.Name],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.priority = priority
        self.mx = str(mx).rstrip('.')
        MXRecord.all_mx_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(MXRecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'mxrecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_mx_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of mxrecord objects written to file
        """
        if MXRecord.all_mx_records:
            cols = MXRecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in MXRecord.all_mx_records:
                    mywriter.writerow(row.__dict__)
        return len(MXRecord.all_mx_records)


class PTRRecord:
    """
    PTR Record or ptrrecord NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-ptrrecord': 'ptrrecord',
        'fqdn': '',
        'dname': '',
        'view': '',
        'ttl': '',
    }
    all_ptr_records: List['PTRRecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 dname: Union[str, dns.name.Name],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.dname = str(dname).rstrip('.')
        PTRRecord.all_ptr_records.append(self)

    @property
    def ip(self) -> str:
        """
        convert DNS reverse name to IP Address

        :return str: string value of IP Address
        """
        name = dns.name.from_text(self.fqdn)
        return dns.reversename.to_address(name)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(PTRRecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'ptrrecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_ptr_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of ptrrecord objects written to file
        """
        if PTRRecord.all_ptr_records:
            cols = PTRRecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in PTRRecord.all_ptr_records:
                    mywriter.writerow(row.__dict__)
        return len(PTRRecord.all_ptr_records)

    def __hash__(self):
        ip = self.ip
        return hash((
            self.dname,
            ip,
            self.view
        ))


class SRVRecord:
    """
    SRV Record or srvrecord NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-srvrecord': 'srvrecord',
        'fqdn': '',
        'priority': '',
        'weight': '',
        'port': '',
        'target': '',
        'view': '',
        'ttl': '',
    }
    all_srv_records: List['SRVRecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 priority: int,
                 weight: int,
                 port: int,
                 target: Union[str, dns.name.Name],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        self.priority = priority
        self.weight = weight
        self.port = port
        self.target = str(target).rstrip('.')
        SRVRecord.all_srv_records.append(self)

    @staticmethod
    def cols() -> list:
        """
        return object csv columns
        :return: list of column headers
        """
        return list(SRVRecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'srvrecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_srv_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of srvrecord objects written to file
        """
        if SRVRecord.all_srv_records:
            cols = SRVRecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in SRVRecord.all_srv_records:
                    mywriter.writerow(row.__dict__)
        return len(SRVRecord.all_srv_records)


class TXTRecord:
    """
    TXT Record or txtrecord NIOS/CSV object class
    """
    DEFAULT_OBJECT = {
        'header-txtrecord': 'txtrecord',
        'fqdn': '',
        'text': '',
        'view': '',
        'ttl': '',
    }
    all_txt_records: List['TXTRecord'] = []

    def __init__(self,
                 fqdn: Union[str, dns.name.Name],
                 text: Union[str, tuple],
                 view: Optional[str] = None,
                 ttl: Optional[int] = None):
        for prop, value in self.DEFAULT_OBJECT.items():
            setattr(self, prop, value)
        self.fqdn = str(fqdn).rstrip('.')
        self.view = view
        self.ttl = ttl
        if isinstance(text, tuple):
            self.text = self.parse_txt_rdata(text)
        else:
            self.text = text
        TXTRecord.all_txt_records.append(self)
        logging.debug(pprint.pformat(self.__dict__))

    @staticmethod
    def cols() -> list:
        """
        return object csv columns

        :return: list of column headers
        """
        return list(TXTRecord.DEFAULT_OBJECT.keys())

    @staticmethod
    def write_csv_file(csvfile: str = 'txtrecords.csv',
                       import_action: bool = False) -> int:
        """
        write all_txt_records to CSV file

        :param csvfile: Infoblox CSV file name
        :param import_action: true if the data contains IMPORT-ACTION column

        :return: number of txtrecord objects written to file
        """
        if TXTRecord.all_txt_records:
            cols = TXTRecord.cols()
            if import_action:
                cols.insert(1, 'IMPORT-ACTION')
            with open(csvfile, 'w', encoding='utf8') as out_file:
                mywriter = csv.DictWriter(out_file, fieldnames=cols)
                mywriter.writeheader()
                for row in TXTRecord.all_txt_records:
                    mywriter.writerow(row.__dict__)
        return len(TXTRecord.all_txt_records)

    @staticmethod
    def parse_txt_rdata(rdata: tuple) -> str:
        """
        parse dns.rdata tuple into space separated double-quoted strings

        :param rdata: rdata tuple object

        :return str: string value of Text field
        """
        logging.debug(rdata)
        text = []
        for x in rdata:
            chunk = x.decode('UTF-8')
            # the next two (2) lines are bluecat network hacks
            if '\"' in chunk:
                chunk = chunk.replace('\"', '')
                chunk = chunk.replace('\\', '')
            text.append(f'"{chunk}"')
        logging.debug(' '.join(text))
        return ' '.join(text)
