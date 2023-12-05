# Record Classes

The record.py module contains a series of classes which facilitate in the 
generation of Infoblox CSV objects from dnspython resource record objects. 
These classes were principally written for the dns_to_ibxcsv.py which has a 
number of different conversion and migration mechanisms which take DNS data 
and converts to Infoblox CSV file(s) used for importing into the Grid. This 
is a relatively new set of classes, that will likely lead to a lot of 
enhancements. 

## Usage

The usage is simple:

```python
from infoblox_pslib.nios.record import ARecord, AAAARecord, MXRecord


# example of iterating over a dnspython zone object and building CSV object(s)
def get_resource_recs(
        zone_object: dns.zone.Zone,
        csv_type: str,
        max_ttl: int,
        view: str) -> list:
    """
    create CSV record object(s) from zone file object(s)

    :param zone_object: dns.zone.Zone object to process
    :param csv_type: Infoblox CSV object type
    :param max_ttl: Max TTL ceiling
    :param view: Infoblox DNS View name
    :return: list of Infoblox CSV object record(s)
    """
    records = []
    rdtype = rdtypes[csv_type]
    for record in zone_object.iterate_rdatas(rdtype):
        name, ttl, rdata = record
        if ttl >= max_ttl:
            ttl = ''
        rec = None
        if csv_type == 'arecord':
            rec = ARecord(name, view, ttl, rdata.address)
        elif csv_type == 'aaaarecord':
            rec = AAAARecord(name, view, ttl, rdata.address)
        elif csv_type == 'cnamerecord':
            rec = CNAMERecord(name, view, ttl, rdata.target)
        elif csv_type == 'dnamerecord':
            rec = DNAMERecord(name, view, ttl, rdata.target)
        elif csv_type == 'mxrecord':
            rec = MXRecord(name, view, ttl, rdata.preference, rdata.exchange)
        elif csv_type == 'ptrrecord':
            rec = PTRRecord(name, view, ttl, rdata.target)
        elif csv_type == 'srvrecord':
            rec = SRVRecord(
                name, view, ttl,
                rdata.priority,
                rdata.weight,
                rdata.port,
                rdata.target
            )
        elif rdtype == dns.rdatatype.TXT:
            rec = TXTRecord(name, view, ttl, rdata.strings)

        if rec:
            records.append(rec)
    return records
```