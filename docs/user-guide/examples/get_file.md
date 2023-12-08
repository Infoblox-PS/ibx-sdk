# Get File

## Overview

This Python script serves as a command-line utility for retrieving files from an Infoblox Grid Manager using the
Infoblox Web API (WAPI). Users can specify key parameters such as the Grid Manager address, the target member from
which to retrieve configuration data, and the type of configuration  (e.g., DNS_CFG, DHCP_CFG) when executing the
script from the command line. Optional parameters include the Infoblox admin username, the option to exclude rotated
logs, and the ability to enable debugging for troubleshooting purposes. Whether you need to access DNS, DHCP, or
other file data from Infoblox, this utility simplifies the process.

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

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DNS_CFG
```

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DHCP_CFG
```

```sh
get-file -u admin -g 192.168.1.2 -m infoblox.localdomain -t DHCPV6_CFG
```
