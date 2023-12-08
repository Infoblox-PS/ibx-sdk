# Grid Restore

## Overview

This Python script is a command-line utility designed to facilitate the restoration of an Infoblox NIOS Grid using the
Infoblox Web API (WAPI). Users can specify essential parameters such as the Grid Manager's IP or hostname and the
filename of the backup to be restored when executing the script via the command line. Optional parameters include the
Infoblox NIOS username, the restoration mode (NORMAL, FORCED, or CLONE), and the option to retain the existing IP
configuration or use the IP settings from the backup. Additionally, the script offers debugging capabilities for
advanced users. Whether you need to recover a previous configuration or clone a Grid setup, this utility simplifies the
restoration process, making it a valuable tool for data recovery and system replication within an Infoblox environment.

## Usage

```
Usage: grid-restore [OPTIONS]

  Restore NIOS Grid.

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox NIOS Grid Manager IP/Hostname  [required]
    -f, --filename TEXT           Infoblox NIOS Grid restore filename  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox NIOS username
    -m, --mode [NORMAL|FORCED|CLONE]
                                  Grid Restore Mode [NORMAL|FORCED|CLONE]  [default: FORCED]
    -k, --keep                    Keep existing IP otherwise use IP from backup
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       Enable verbose logging
  -h, --help                      Show this message and exit.

```

## Example

```sh
grid-restore -u admin -g 192.168.1.2 -f database.bak -m FORCED -k
```

