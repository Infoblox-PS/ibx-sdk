# CSV Export

## Overview

This Python program is a command-line utility designed to simplify the process of exporting data
from an Infoblox Grid Manager using the Infoblox Web API (WAPI) and saving it to a CSV file. With 
this tool, users can specify essential parameters like the Grid Manager address, the desired output 
file name, and their authentication credentials. Additionally, it provides flexibility by allowing 
users to specify options such as the Infoblox WAPI version and the type of Infoblox objects to 
export. Whether you need to extract network information, DNS records, or other data managed
by Infoblox, this utility streamlines the process, making it a valuable resource for Infoblox
administrators and users who need to work with data in CSV format.

## Usage

To invoke the usage run `csvexport --help`

```
Usage: csvexport [OPTIONS]

  CSV Export by object

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
    -f, --file TEXT      Infoblox WAPI CSV export file name  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
    -o, --object TEXT    WAPI export object type
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.
```

## Example

### CSV Export

```shell
csvexport -u admin -g 192.168.1.2 -f ibcsv-networks.csv -o network
```

The command invokes the CSV Job Manager and creates a job to export objects of type network. Once
the job is complete,
the data is exported and saved.

**Screen output from command**

```text
Enter password for [admin]:
2023-12-09 12:36:27 [nios_csvexport.py:88] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 12:36:27 [fileop.py:154] INFO performing csv export for network object(s)
2023-12-09 12:36:27 [fileop.py:177] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209183627629530/Networks.csv
2023-12-09 12:36:27 [fileop.py:187] INFO writing data to ibcsv_networks.csv file
2023-12-09 12:36:27 [fileop.py:719] INFO file ibcsv_networks.csv download complete
```

**Output from ibcsv-networks.csv**

```text
header-network,address*,netmask*,always_update_dns,basic_polling_settings,boot_file,boot_server,broadcast_address,comment,ddns_domainname,ddns_ttl,deny_bootp,dhcp_members,disabled,discovery_exclusion_range,discovery_member,domain_name,domain_name_servers,enable_ddns,enable_discovery,enable_option81,enable_pxe_lease_time,enable_threshold_email_warnings,enable_threshold_snmp_warnings,enable_thresholds,generate_hostname,ignore_client_requested_options,is_authoritative,lease_scavenge_time,lease_time,mgm_private,network_view,next_server,option_logic_filters,pxe_lease_time,range_high_water_mark,range_high_water_mark_reset,range_low_water_mark,range_low_water_mark_reset,recycle_leases,routers,threshold_email_addresses,update_dns_on_lease_renewal,update_static_leases,vlans,zone_associations
network,100.64.50.0,255.255.255.0,,,,,,,,,,ns1.ffy.network,False,,nd.ffy.network,ffy.corp,"100.64.50.53,100.64.50.54",,True,,,False,False,,,,,,,False,default,,,,95,85,0,10,,100.64.50.1,,,,,<empty>
network,100.64.40.0,255.255.255.0,,,,,,,,,,,False,,nd.ffy.network,,,,True,,,False,False,,,,,,,False,default,,,,95,85,0,10,,,,,,,<empty>
```
   
