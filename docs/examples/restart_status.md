# Restart Status

## Overview

This Python script is a command-line utility that allows users to retrieve the restart status of
Infoblox NIOS Protocol Services using the Infoblox Web API (WAPI). After specifying essential 
parameters such as the Grid Manager's address and optional parameters like the Infoblox admin 
username and WAPI version, users can execute the script via the command line. The script then 
connects to the Infoblox grid manager and fetches the restart status, providing valuable insights
into the current state of protocol services. This tool simplifies monitoring and troubleshooting of
Infoblox services, helping network administrators ensure the reliability and stability of their 
network infrastructure.

## Usage

To invoke the usage run `nios-restart-status --help`

```
Usage: nios-restart-status [OPTIONS]

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

