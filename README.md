<img alt="Professional Services" src="docs/assets/ib-toolkit-img.png" title="Infoblox Professional Services"/>

# Table of Contents

1. [NIOS API](#nios-api)
2. [Overview](#overview)

# Overview

A collection of basic tools and functions used by other integrations written by Infoblox Professional Services. This
collection also contains scripts that perform various functions. These scripts are written as functioning examples.

# NIOS API

## WAPI Module Overview

The `wapy.py` is a Python class library designed for interacting with the Infoblox NIOS Web API (WAPI). The primary
class,
`WAPI`, extends `requests.sessions.Session` and provides functionalities for session management, data retrieval, file
operations, and service management

### Key Classes and Literals

- **WAPI**: This is the main class handling interactions with the Infoblox WAPI. It includes methods for CRUD (Create,
  Read, Update, Delete) operations, grid management, service restarts, and fetching log files.
- **BaseWapiException**: A base exception class for WAPI-related errors.
- **WapiRequestException**: A subclass of `BaseWapiException` specifically for handling request errors.
- **ServiceRestartOption**: A literal representing service restart options.
- **ServiceRestartServices**: A literal indicating the services that can be restarted.
- **ServiceRestartMode**: Describes the mode of service restart.
- **CsvOperation**: Represents different operations that can be performed on CSV files.
- **GridRestoreMode**: Indicates the modes available for grid restoration.
- **MemberDataType**: Defines the types of data that can be associated with a grid member.
- **LogType**: Specifies the types of logs that can be retrieved.

### Key Methods of `WAPI`

- **Connection Management**: `connect()`
- **Data Retrieval**: `get()`, `object_fields()`
- **Data Modification**: `post()`, `put()`
- **File Operations**: `csv_export()`, `csv_import()`, `grid_restore()`, `grid_backup()`
- **Service Management**: `service_restart()`, `get_service_restart_status()`
- **Log Management**: `get_log_files()`, `get_support_bundle()`

### Example Usage

Here's an example of how to use the `WAPI` class:

```python
# Initialize the WAPI instance
wapi = WAPI(grid_mgr='10.0.0.1', username='admin', password='infoblox', wapi_ver='2.5', ssl_verify=False)

# Connect to the grid
wapi.connect()

# Retrieve object fields
fields = wapi.object_fields('record:host')
if fields is not None:
   print(f"Fields: {fields}")

# Example POST request
response = wapi.post('https://example.com/api/resource', data={'key': 'value'})
print(response.status_code)
```

## FILEOP Module Overview

The `fileop.py` module provides a suite of functions for managing file operations in the context of the Infoblox Web
API (WAPI). These functions are designed to be used within the `WAPI` class and handle various file-related tasks
such as configuration file downloads, CSV exports and imports, grid backups and restorations, and log file management.

### Key Functions

- **member_config**: Downloads a configuration file for a specific grid member.
- **csv_export**: Exports data from the WAPI to a CSV file.
- **csv_import**: Imports data from a CSV file into the WAPI.
- **grid_backup**: Backs up the Infoblox Grid and saves it to a local file.
- **grid_restore**: Restores the Infoblox Grid database from a backup file.
- **get_support_bundle**: Fetches a support bundle from an Infoblox member.
- **get_log_files**: Retrieves specified log files from the NIOS system.

### Internal Helper Functions

- **_upload_init**: Initializes a file upload to the Infoblox WAPI.
- **__upload_file**: Uploads a file to the specified URL using the Infoblox WAPI.
- **__csv_import**: Performs a CSV import job via WAPI.
- **csvtask_status**: Fetches the status of a CSV import task from the CSV Job Manager.
- **get_csv_errors_file**: Downloads the CSV errors file for a specified job.
- **__getgriddata**: Executes a 'getgriddata' file operation call to the Infoblox WAPI.
- **__download_file**: Downloads a file from a specified Infoblox URL.
- **__download_complete**: Notifies the completion of a file download process in the Infoblox WAPI.
- **__restore_database**: Performs a database restore operation in the Infoblox WAPI.

### Example Usage

```python
# Initialize WAPI instance
wapi_instance = WAPI(...)

# Download a member configuration file
config_file = wapi_instance.member_config(
   member='grid-member.example.com',
   conf_type='DNS'
)

# Export data to CSV
wapi_instance.csv_export('network', 'network_data.csv')

# Import data from CSV
csv_task = wapi_instance.csv_import('IMPORT', '/path/to/import.csv')

# Perform a Grid backup
wapi_instance.grid_backup('grid_backup.tgz')

# Restore Grid from a backup file
wapi_instance.grid_restore('grid_backup.tgz', 'NORMAL', True)

# Fetch a support bundle
wapi_instance.get_support_bundle(member='grid-member.example.com')

# Retrieve log files
wapi_instance.get_log_files(log_type='syslog', member='grid-member.example.com')
```

## Grid Services Module Overview

The `Grid Services` module in Python provides functions to interact with and manage services in an Infoblox Grid
environment. It includes capabilities to restart services, update their status, and retrieve the status of service
restarts.

### Key Functions

1. **service_restart**: Restarts specified services of a group, member, or all services on the grid.
    - **Arguments**: Accepts arbitrary keyword arguments to specify services to restart.
    - **Return Value**: None. Logs the result of the operation.
    - **Exception**: Raises `requests.exceptions.RequestException` for request-related errors.

2. **update_service_status**: Updates the restart status of specified grid services.
    - **Arguments**: `services` (str) - specifies the services to check the restart status for. Defaults to 'ALL'.
    - **Return Value**: None. Logs the response text upon successful completion of the request.
    - **Exception**: Raises `requests.exceptions.RequestException` for request-related errors.

3. **get_service_restart_status**: Retrieves the restart status of all member services.
    - **Return Value**: Returns a dictionary containing the restart status of all member services.
    - **Exception**: Raises `requests.exceptions.SSLError`, `requests.exceptions.HTTPError`,
      or `requests.exceptions.RequestException` for various request-related errors.

### Example Usage

```python
# Initialize the WAPI instance
wapi_instance = WAPI(...)

# Restart all services
wapi_instance.service_restart(services='ALL')

# Update the service status
wapi_instance.update_service_status('DNS')

# Get service restart status
status = wapi_instance.get_service_restart_status()
print(status)
```
## Logger functions

* init_logger
* init_console_logger
* increase_log_level
* set_log_level

## Scripts Folder


