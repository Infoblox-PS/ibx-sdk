# Restart Status

## Overview

This program is a command-line utility designed to retieve the restart services 
status from the Grid Manager.

## Usage

```
Usage: restart-status [OPTIONS]

  Retrieve Restart Status

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.

```

## Example

```sh
restart-status -u admin -g 192.168.1.2
```

