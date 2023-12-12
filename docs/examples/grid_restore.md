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

## Examples

### Restore Grid Backup from File

The following example will restore a backup a Grid Manager.

```sh
grid-restore -u admin -g 192.168.1.2 -f database.bak -m NORMAL
```

**Screen output from command**

```text
grid-restore -u admin -g 192.168.1.2 -f database.bak -m NORMAL
Enter password for [admin]: 
2023-12-09 20:45:21 [nios_grid_restore.py:94] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 20:45:21 [fileop.py:830] INFO step 1 - request uploadinit database.bak
2023-12-09 20:45:22 [fileop.py:846] INFO step 2 - post the files using the upload_url provided
2023-12-09 20:45:25 [fileop.py:855] INFO step 3 - execute the restore
2023-12-09 20:45:35 [fileop.py:867] INFO Grid restore successful!
```

!!! Danger

    Restoring an Infoblox Grid should only be considered as a final option for production deployments. Please refrain from
    initiating a restoration process unless you are in a Disaster Recovery (DR) scenario or directed to do so by
    Infoblox Technical Support.

### Restore Grid Backup from file to a Lab

The following example will restore a backup of a Grid Manager to another system (lab).

```sh
grid-restore -u admin -g 192.168.1.3 -f database.bak -m FORCED -k
```

**Screen output from command**

```text
grid-restore -u admin -g 192.168.1.3 -f database.bak -m FORCED -k
Enter password for [admin]: 
2023-12-09 20:57:51 [nios_grid_restore.py:94] INFO connected to Infoblox grid manager  192.168.1.3
2023-12-09 20:57:51 [fileop.py:830] INFO step 1 - request uploadinit database.bak
2023-12-09 20:57:51 [fileop.py:846] INFO step 2 - post the files using the upload_url provided
2023-12-09 20:57:53 [fileop.py:855] INFO step 3 - execute the restore
2023-12-09 20:58:02 [fileop.py:867] INFO Grid restore successful!

```
