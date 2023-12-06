<img alt="Professional Services" src="images/ib-toolkit-img.png" title="Infoblox Professional Services"/>

# ibx-tools

A collection of basic tools and functions used by other integrations in the Infoblox environment.

## Table of Contents

1. [Base Toolkit](#base-toolkit)
2. [License](#license-type)
3. [Code Review](#code-review)
4. [Git Restrictions](#git-restrictions)
5. [Documentation](#documentation)

# Base Toolkit

## NIOS funtions

* wapi api wrapper
* fileop
* services

## Logger functions

## utilities functions

* named_checkconf
* named_compilezone

## Scripts Folder

* [nios-csvimport](#nios-csv-import)
* [nios-csvexport](#nios-csv-export)
* [nios-get-log](#nios-get-log)
* [nios-get-supportbundle](#nios-get-support-bundle)
* [nios-grid-backup](#nios-grid-backup)
* [nios-grid-restore](#nios-grid-restore)
* [nios-restart-service](#nios-restart-services)
* [nios-restart-status](#nios-restart-services)

## License Type
- Perhaps MIT

## Code Review
Please see issue https://github.com/Infoblox-PS/ibx-tools/issues/1

## Git Restrictions

- Do we enable/disable abilty to open issues/rfes/etcn
- Public/Not Public
- Who are the maintainers

## Documentation

### NIOS CSV Import

Usage:

```
Usage: nios-csvimport [OPTIONS]

  CSV Import Data

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
    -f, --file TEXT               Infoblox WAPI CSV import file name  [required]
    -o, --operation [INSERT|OVERRIDE|MERGE|DELETE|CUSTOM]
                                  CSV import mode  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.

```

### NIOS CSV Export

Usage:

```
Usage: nios-csvexport [OPTIONS]

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

### NIOS Get Log

Usage:

```
Usage: nios-get-log [OPTIONS]

  Retrieve Log from NIOS Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
    -m, --member TEXT             Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -t, --log-type TEXT           SYSLOG | AUDITLOG | MSMGMTLOG |DELTALOG | OUTBOUND |
                                  PTOPLOG |DISCOVERY_CSV_ERRLOG]  [default: SYSLOG]
    -n, --node-type [ACTIVE|PASSIVE]
                                  Node: ACTIVE | PASSIVE  [default: ACTIVE]
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.

```

### NIOS Get Support Bundle

Usage:

```
Usage: nios-get-supportbundle [OPTIONS]

  Retrieve Support Bundle from Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT         Infoblox Grid Manager  [required]
    -m, --member TEXT           Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT         Infoblox admin username  [default: admin]
    -r, --rotated-logs BOOLEAN  Include Rotated Logs  [default: True]
    -l, --logs-files BOOLEAN    Include Log Files  [default: True]
    -w, --wapi-ver TEXT         Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                     enable verbose debug output
  -h, --help                    Show this message and exit.
```

### NIOS Grid Backup

Usage:

```
Usage: nios-grid-backup [OPTIONS]

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

### NIOS Grid Restore

Usage:

```
Usage: nios-grid-restore [OPTIONS]

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
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.

```

### NIOS Restart Services

Usage:

```
Usage: nios-restart-service [OPTIONS]

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

### NIOS Restart Status

Usage:

```
Usage: nios-restart-status [OPTIONS]

  RRetrieve Restart Status

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

- How to upload your python package to PyPi https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
