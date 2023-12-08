# Get Log

## Overview

This Python script is a command-line utility designed to simplify the process of retrieving logs from an Infoblox Grid
Manager using the Infoblox Web API (WAPI). Users can specify key parameters such as the Grid Manager address, the target
member to retrieve logs from, and the log type (e.g., SYSLOG) when executing the script from the command line.
Additionally, optional parameters include the Infoblox admin username, node type (ACTIVE or PASSIVE), and the ability to
exclude rotated logs. The script also provides debugging capabilities for enhanced troubleshooting. Whether you need to
access system logs or specific log types, this utility streamlines the process, making it a valuable tool for managing
and analyzing logs within an Infoblox environment.

## Usage

```
Usage: get-log [OPTIONS]

  Get NIOS Log from Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
    -m, --member TEXT             Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -t, --log-type LOG_TYPE       select log type  [default: SYSLOG]
    -n, --node-type [ACTIVE|PASSIVE]
                                  Node: ACTIVE | PASSIVE  [default: ACTIVE]
    -r, --rotated-logs            Exclude Rotated Logs
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.
```

## Examples

```sh
get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t SYSLOG
```

```sh
get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t AUDIT_LOG
```

```sh
get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t MSMGMTLOG
```