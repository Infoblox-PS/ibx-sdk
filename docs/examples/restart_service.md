# Restart Services

## Overview

This Python script is a command-line utility designed to streamline the process of restarting Infoblox NIOS Protocol
Services using the Infoblox Web API (WAPI). Users can specify essential parameters such as the Grid Manager's address
and the service to be restarted (DNS, DHCP, DHCPv4, DHCPv6, or all services) when executing the script via the command
line. Optional parameters include the Infoblox admin username and the ability to customize the Infoblox WAPI version.
Additionally, the script offers debugging capabilities for advanced users. Whether you need to restart specific services
or all services within your Infoblox environment, this utility simplifies the process, making it a valuable tool for
maintaining the health and performance of your network infrastructure.

## Usage

```
Usage: restart-service [OPTIONS]

  Restart NIOS Protocol Services

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -s, --service [DNS|DHCP|DHCPV4|DHCPV6|ALL]
                                  select which service to restart  [default: ALL]
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.
```

## Example

### Restart ALL Services

The following example restart all services (DNS,DHCP,DHCPV6).

```sh
grid-restore -u admin -g 192.168.1.2
```
**Screen output from command**

```text
restart-service -u admin -g 192.168.1.2 
Enter password for [admin]: 
2023-12-09 21:04:03 [nios_restart_service.py:89] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 21:04:03 [service.py:65] INFO successfully restarted ['ALL'] services
```
### Restart DNS Services

The following example restart DNS services.

```sh
grid-restore -u admin -g 192.168.1.2 -s DNS
```
**Screen output from command**

```text
 restart-service -u admin -g 100.64.40.40 -s DNS
Enter password for [admin]: 
2023-12-09 21:04:52 [nios_restart_service.py:89] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 21:04:52 [service.py:65] INFO successfully restarted ['DNS'] services
```

### Restart DHCP Services

The following example restart DHCP services.

```sh
grid-restore -u admin -g 192.168.1.2 -s DHCP
```

**Screen output from command**

```text
restart-service -u admin -g 192.168.1.2 -s DHCP
Enter password for [admin]: 
2023-12-09 21:05:18 [nios_restart_service.py:89] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 21:05:18 [service.py:65] INFO successfully restarted ['DHCP'] services
```

### Restart DHCPV6 Services

The following example restart DHCPV6 services.

```sh
grid-restore -u admin -g 192.168.1.2 -s DHCPV6
```

**Screen output from command**

```text
restart-service -u admin -g 192.168.1.2 -s DHCPV6
Enter password for [admin]: 
2023-12-09 21:09:10 [nios_restart_service.py:89] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 21:09:10 [service.py:65] INFO successfully restarted ['DHCPV6'] services
```
