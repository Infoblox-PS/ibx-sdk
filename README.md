<img alt="Professional Services" src="images/ib-toolkit-img.png" title="Infoblox Professional Services"/>

# ibx-tools

A collection of basic tools and functions used by other integrations in the Infoblox environment.

# Table of Contents

1. [Base Toolkit](#base-toolkit)
2. [License](#license-type)
3. [Code Review](#code-review)
4. [Git Restrictions](#git-restrictions)
5. [Documentation](#documentation)

# Base Toolkit

## NIOS funtions
## Overview of the WAPI Class

### Description
The WAPI class is a comprehensive Python API class designed for managing and interacting with Infoblox WAPI calls. It includes functionalities like managing grid members, performing file operations, handling CSV tasks, and service management. This class is part of a larger suite of tools under the `ibx_tools.nios` module.

### Key Features
1. **Session Management:** Inherits from `requests.sessions.Session` for HTTP session handling.
2. **Grid Manager Connectivity:** Connects to Infoblox grid managers, handles authentication, and manages API interactions.
3. **Exception Handling:** Custom exception classes `BaseWapiException` and `WapiRequestException` for error handling.
4. **Data Retrieval and Management:** Methods for fetching object fields, grid member configurations, log files, and support bundles.
5. **CSV Operations:** Support for importing and exporting CSV data, including task status checks and error file retrievals.
6. **Grid and Member Services Management:** Functionality for grid backup and restore, service restarts, and fetching service restart status.

### Method Summary
- **Initialization and Connection:** `__init__`, `__repr__`, `url`, `connect`
- **Data Retrieval:** `object_fields`, `max_wapi_ver`, `get`, `post`, `put`, `get_service_restart_status`, `get_log_files`
- **File Operations:** `member_config`, `csv_export`, `csv_import`, `csv_task_status`, `get_csv_errors_file`, `grid_restore`, `grid_backup`, `get_support_bundle`
- **Service Management:** `service_restart`

### Usage Examples
- **Initialization:** `wapi = WAPI(grid_mgr='10.0.0.1', username='admin', password='infoblox', wapi_ver='2.5', ssl_verify=False)`
- **Object Fields Retrieval:** `fields = wapi.object_fields('record:host')`
- **CSV Import:** `response = wapi.csv_import('INSERT', 'path/to/file.csv')`
- **Grid Backup:** `wapi.grid_backup('backup.tgz')`
- **Service Restart:** `wapi.service_restart(groups=['group1', 'group2'], services=['DNS', 'DHCP'])`

### Notes
- The class disables urllib3 warnings about unverified HTTPS requests, considering `ssl_verify` defaults to `False`.
- It uses the `logging` module for debugging and error logging.
- Detailed docstrings provide guidance on method usage and examples.

### Dependencies
- `requests`: For HTTP requests.
- `typing`: For type annotations.
- `ibx_tools.nios`: For file and service operations.

## Fileop Class Documentation

## Overview
The `Fileop` class provides various file operation functionalities related to Infoblox Web API (WAPI). It includes methods to handle config file downloads, CSV exports and imports, grid backup and restore, support bundle fetch, and log file retrieval.

---

## Methods

### member_config
- **Purpose**: Downloads a member config file for DNS, DHCP, or DHCP6.
- **Parameters**:
  - `member` (str): Fully Qualified Domain Name of the grid member.
  - `conf_type` (str): Type of configuration ('DNS', 'DHCP_CONFIG', 'DHCP6_CONFIG').
  - `remote_url` (str, optional): Alternate download location URL.
- **Returns**: Filename of the downloaded config file.

### csv_export
- **Purpose**: Performs Infoblox CSV Export to a file.
- **Parameters**:
  - `wapi_object` (str): CSV object type to export.
  - `filename` (str, optional): Output CSV file name.
- **Returns**: None. Writes data to a file.

### csv_import
- **Purpose**: Initiates a CSV import job via WAPI.
- **Parameters**:
  - `task_operation` (str): Operation type (e.g., 'IMPORT', 'UPDATE').
  - `csv_import_file` (str): Path to the CSV file.
  - `exit_on_error` (bool, optional): Halts on error if True.
- **Returns**: Dictionary representing the status of the CSV import job.

### grid_backup
- **Purpose**: Performs a backup of the Infoblox Grid and saves it to a file.
- **Parameters**:
  - `filename` (str, optional): Name/path of the backup file.
- **Returns**: None. Saves the file locally.

### grid_restore
- **Purpose**: Restores the Infoblox NIOS database from a backup file.
- **Parameters**:
  - `restore_file_name` (str): Backup file name/path.
  - `mode` (str): Restore mode ('NORMAL', 'FORCED', or 'CLONE').
  - `keep_grid_ip` (bool): Retain Grid Manager's IP settings if True.
- **Returns**: None. Performs the restore operation.

### get_support_bundle
- **Purpose**: Fetches and downloads a support bundle from an Infoblox member.
- **Parameters**:
  - `member` (str): Target member name/IP.
  - Various boolean flags to include specific data in the bundle.
  - `remote_url` (str, optional): Remote server URL for the bundle.
  - `rotate_log_files` (bool, optional): Rotate log files after bundle creation.
- **Returns**: None. Saves the support bundle file.

### get_log_files
- **Purpose**: Fetches specified log files from NIOS and writes them to disk.
- **Parameters**:
  - `log_type` (str): Type of log files.
  - Additional optional parameters to specify endpoint, member, etc.
- **Returns**: None. Fetches and saves the log files.

---

## Notes
- The class includes various private methods (`_upload_init`, `_upload_file`, `_csv_import`, etc.) to support the main functionalities.
- These methods handle different stages of file operations, including initialization, upload, download, and completion notifications.
- Exception handling is integrated into each method to catch and log errors during HTTP requests.

---

<<<<<<< Updated upstream
* wapi
* fileop
=======
>>>>>>> Stashed changes
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
