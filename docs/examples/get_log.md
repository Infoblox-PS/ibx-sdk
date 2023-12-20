# Get Log

## Overview

This Python script is a command-line utility designed to simplify the process of retrieving logs
from an Infoblox Grid Manager using the Infoblox Web API (WAPI). Users can specify key parameters 
such as the Grid Manager address, the target member to retrieve logs from, and the log type 
(e.g., SYSLOG) when executing the script from the command line. Additionally, optional parameters
include the Infoblox admin username, node type (ACTIVE or PASSIVE), and the ability to exclude
rotated logs. The script also provides debugging capabilities for enhanced troubleshooting.
Whether you need to access system logs or specific log types, this utility streamlines the process,
making it a valuable tool for managing and analyzing logs within an Infoblox environment.

## Usage

To invoke the usage run `nios-get-log --help`

```
Usage: nios-get-log [OPTIONS]

  Get NIOS Log from Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
    -m, --member TEXT             Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -t, --log-type LOG_TYPE       select log type  [default: SYSLOG]
    -n, --node-type [ACTIVE|PASSIVE]
                                  Node: ACTIVE | PASSIVE  [default: ACTIVE]
    -r, --rotated-logs            Exclude Rotated Logs
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.
```

## Examples

### Syslog Download

The following example will download the SYSLOG file from the infoblox.localdomain.

```sh
nios-get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t SYSLOG
```

**Screen output from command**

```text
nios-get-log -u admin -g 192.168.1.2 -m infoblox.localdomain -t SYSLOG
Enter password for [admin]: 
2023-12-09 17:13:42 [nios_get_log.py:108] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 17:13:42 [fileop.py:982] INFO fetching SYSLOG log files for infoblox.localdomain
2023-12-09 17:13:48 [fileop.py:1019] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1209231342096359/sysLog.tar.gz
2023-12-09 17:13:48 [fileop.py:1029] INFO writing data to 2023120948-infoblox.localdomain-SYSLOG.tgz file
2023-12-09 17:13:51 [fileop.py:719] INFO file 2023120948-infoblox.localdomain-SYSLOG.tgz download complete
2023-12-09 17:13:51 [nios_get_log.py:115] INFO finished!
```

### Audit Log Download

The following example will download the AUDITLOG file from the infoblox.localdomain.

```sh
nios-get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t AUDITLOG
```

**Screen output from command**

```text
nios-get-log -u admin -g 192.168.1.2 -u admin -m infoblox.localdomain -t AUDITLOG
Enter password for [admin]: 
2023-12-09 19:13:02 [nios_get_log.py:122] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 19:13:02 [fileop.py:1008] INFO fetching AUDITLOG log files for infoblox.localdomain
2023-12-09 19:13:02 [fileop.py:1045] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1210011302085953/auditLog.tar.gz
2023-12-09 19:13:02 [fileop.py:675] INFO https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1210011302085953/auditLog.tar.gz
2023-12-09 19:13:02 [fileop.py:41] INFO writing file: 2023120902-infoblox.localdomain-AUDITLOG.tgz
2023-12-09 19:13:02 [fileop.py:727] INFO file 2023120902-infoblox.localdomain-AUDITLOG.tgz download complete
2023-12-09 19:13:02 [nios_get_log.py:129] INFO finished!
```

