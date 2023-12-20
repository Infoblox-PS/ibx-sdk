# Grid Backup

## Overview

This Python script serves as a command-line utility for creating a backup of an Infoblox NIOS Grid
using the Infoblox Web API (WAPI). Users can specify key parameters such as the Grid Manager address 
and the desired backup file name when executing the script from the command line. Optional 
parameters include the Infoblox admin username and the ability to customize the Infoblox WAPI 
version. The script also offers debugging capabilities for advanced users. Whether you need to
safeguard the configuration and data of your Infoblox NIOS Grid, this utility simplifies the
process, making it a valuable tool for data protection and disaster recovery.

## Usage

To invoke the usage run `nios-grid-backup --help`

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

## Example

### Create and Download Grid Backup

The following example will download backup of the Grid Manager.

```sh
grid-backup -u admin -g 192.168.1.2 -f database.bak
```

**Screen output from command**

```text
grid-backup -u admin -g 192.168.1.2 -f database.bak
Enter password for [admin]: 
2023-12-09 20:40:55 [nios_grid_backup.py:85] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 20:40:55 [fileop.py:618] INFO step 1 - request gridbackup database.bak
2023-12-09 20:40:58 [fileop.py:628] INFO step 2 - saving backup to database.bak
2023-12-09 20:40:58 [fileop.py:675] INFO https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1210024055568763/database.bak
2023-12-09 20:40:58 [fileop.py:41] INFO writing file: database.bak
2023-12-09 20:40:59 [fileop.py:727] INFO file database.bak download complete
```
