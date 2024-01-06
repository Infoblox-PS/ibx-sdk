# Get File

## Overview

This Python program is a command-line utility designed to retrieve configuration files from the 
Grid.

## Usage

```
Usage: get-file [OPTIONS]

  Get NIOS File

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
    -m, --member TEXT    Member to retrieve file from  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -t, --cfg-type TEXT  Configuration Type: DNS_CACHE | DNS_CFG | DHCP_CFG | DHCPV6_CFG |
                         TRAFFIC_CAPTURE_FILE | DNS_STATS | DNS_RECURSING_CACHE  [default:
                         DNS_CFG]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.

```

## Examples

### DNS Configuration Download

The following example will download the named.conf file from the infoblox.localdomain.

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DNS_CFG
```

**Screen output from command**

```text
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DNS_CFG 
Enter password for [admin]: 
2023-12-09 16:56:51 [nios_get_file.py:94] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 16:56:51 [fileop.py:65] INFO fetching DNS_CFG config file for grid member infoblox.localdomain
2023-12-09 16:56:51 [fileop.py:91] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209225651240725/dnsConf.tar.gz
2023-12-09 16:56:51 [fileop.py:100] INFO writing data to dnsconf.tar.gz file
2023-12-09 16:56:51 [fileop.py:719] INFO file dnsconf.tar.gz download complete
2023-12-09 16:56:51 [nios_get_file.py:98] INFO finished!
```

### DHCP Configuration Download

The following example will download the dhcpd.conf file from the infoblox.localdomain.

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DHCP_CFG
```

**Screen output from command**

```text
get-file -u admin -g 192.168.1.2 -m ns1.ffy.network -t DHCP_CFG          
Enter password for [admin]: 
2023-12-09 16:54:44 [nios_get_file.py:94] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 16:54:44 [fileop.py:65] INFO fetching DHCP_CFG config file for grid member infoblox.localdomain
2023-12-09 16:54:44 [fileop.py:91] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209225444728578/dhcpConf.tar.gz
2023-12-09 16:54:45 [fileop.py:100] INFO writing data to dhcpconf.tar.gz file
2023-12-09 16:54:45 [fileop.py:719] INFO file dhcpconf.tar.gz download complete
2023-12-09 16:54:45 [nios_get_file.py:98] INFO finished!
```

### DHCPV6 Configuration Download

The following example will download the dhcpv6.conf file from the infoblox.localdomain.

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DHCPV6_CFG
```

**Screen output from command**

```text
get-file -u admin -g 192.168.1.2 -m ns1.ffy.network -t DHCPV6_CFG        
Enter password for [admin]: 
2023-12-09 17:03:59 [nios_get_file.py:94] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 17:03:59 [fileop.py:65] INFO fetching DHCPV6_CFG config file for grid member infoblox.localdomain
2023-12-09 17:04:00 [fileop.py:91] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209230400019222/dhcpv6Conf.tar.gz
2023-12-09 17:04:00 [fileop.py:100] INFO writing data to dhcpv6conf.tar.gz file
2023-12-09 17:04:00 [fileop.py:719] INFO file dhcpv6conf.tar.gz download complete
2023-12-09 17:04:00 [nios_get_file.py:98] INFO finished!
```

### DNS States

The following example will download the named.stats file from the infoblox.localdomain.

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DNS_STATS
```

**Screen output from command**

```text
get-file -u admin -g 192.168.1.2 -m ns1.ffy.network -t DNS_STATS 
Enter password for [admin]: 
2023-12-09 17:05:10 [nios_get_file.py:94] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 17:05:10 [fileop.py:65] INFO fetching DNS_STATS config file for grid member infoblox.localdomain
2023-12-09 17:05:11 [fileop.py:91] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209230510855236/dnsStats.tar.gz
2023-12-09 17:05:11 [fileop.py:100] INFO writing data to dnsstats.tar.gz file
2023-12-09 17:05:11 [fileop.py:719] INFO file dnsstats.tar.gz download complete
2023-12-09 17:05:11 [nios_get_file.py:98] INFO finished!
```

!!! warning

    Configuration files can only be downloaded if the file exists on the appliance. If the file 
    does not exist a "400 Client Error: Bad Request for url" will be received.
