# Grid Backup

# Overview

This Python script serves as a command-line utility for creating a backup of an Infoblox NIOS Grid using the Infoblox
Web API (WAPI). Users can specify key parameters such as the Grid Manager address and the desired backup file name when
executing the script from the command line. Optional parameters include the Infoblox admin username and the ability to
customize the Infoblox WAPI version. The script also offers debugging capabilities for advanced users. Whether you need
to safeguard the configuration and data of your Infoblox NIOS Grid, this utility simplifies the process, making it a
valuable tool for data protection and disaster recovery.

## Usage

```
Usage: grid-backup [OPTIONS]

  Backup NIOS Grid

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -f, --file TEXT      Infoblox backup file name  [default: database.bak]
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.
```

## Example

```sh
get-supportbundle -u admin -g 192.168.1.2
```
