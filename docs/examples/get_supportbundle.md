# Get Support Bundle

## Overview

This Python script serves as a command-line utility for retrieving a Support Bundle from an Infoblox Grid Manager using
the Infoblox Web API (WAPI). Users can specify essential parameters such as the Grid Manager address and the target
member from which to retrieve the Support Bundle when executing the script from the command line. Optional parameters
include the Infoblox admin username and the ability to include rotated logs and log files in the Support Bundle.
Additionally, the script offers debugging capabilities for advanced users. Whether you need to gather diagnostic
information, including logs and configuration files, from an Infoblox member, this utility simplifies the process,
making it a valuable tool for troubleshooting and support purposes.

# Usage

```
Usage: get-supportbundle [OPTIONS]

  Retrieve Support Bundle from Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
    -m, --member TEXT    Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -r, --rotated-logs   Include Rotated Logs
    -l, --log-files      Include Log Files
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.

```

## Example

```sh
get-supportbundle -u admin -g 192.168.1.2 -m infoblox.localdomain -r -l
```

