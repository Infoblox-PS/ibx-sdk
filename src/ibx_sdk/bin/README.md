## Scripts Documentation

### NIOS Get Config

Usage:

```
Usage: get-config [OPTIONS]

  Get NIOS Configuration from Member

Options:
  Required Parameters: 
    -g, --grid-mgr TEXT  Infoblox Grid Manager  [required]
    -m, --member TEXT    Member to retrieve log from  [required]
  Optional Parameters: 
    -u, --username TEXT  Infoblox admin username  [default: admin]
    -t, --cfg-type TEXT  Configuration Type: DNS_CACHE | DNS_CFG | DHCP_CFG | DHCPV6_CFG |
                         TRAFFIC_CAPTURE_FILE | DNS_STATS | DNS_RECURSING_CACHE  [default:
                         DNS_CFG]
    -r, --rotated-logs   Exclude Rotated Logs
    -w, --wapi-ver TEXT  Infoblox WAPI version  [default: 2.11]
  Logging Parameters: 
    --debug              enable verbose debug output
  -h, --help             Show this message and exit.

```

### NIOS CSV Import

Usage:

```
Usage: csvimport [OPTIONS]

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
Usage: csvexport [OPTIONS]

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
Usage: get-log [OPTIONS]

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
Usage: get-supportbundle [OPTIONS]

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

### NIOS Grid Restore

Usage:

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
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.

```

### NIOS Restart Services

Usage:

```
Usage: restart-service [OPTIONS]

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
Usage: restart-status [OPTIONS]

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

### NIOS Generate CSR

Usage:

```
Usage: generate-csr [OPTIONS]

  Get NIOS Log from Member

Options:
  Required Parameters:
    -g, --grid-mgr TEXT           Infoblox Grid Manager  [required]
    -n, --common-name TEXT        Common Name for the certificate  [required]
    -m, --member TEXT             Member for the certificate  [required]
  Optional Parameters:
    -u, --username TEXT           Infoblox admin username  [default: admin]
    -w, --wapi-ver TEXT           Infoblox WAPI version  [default: 2.11]
  Optional Certificate Parameters:
    -a, --algorithm [SHA-256|SHA-384|SHA-512]
                                  The digest algorithm  [default: SHA-256]
    --certificate-usage [ADMIN|CAPTIVE_PORTAL|SFNT_CLIENT_CERT|IFMAP_DHCP]
                                  Certificate Usage  [default: ADMIN]
    -c, --comment TEXT            Certificate comment
    --country TEXT                Certificate country  [default: US]
    -e, --email TEXT              Certificate email address
    -k, --key-size INTEGER        Certificate key size  [default: 2048]
    -l, --locality TEXT           Certificate locality
    -o, --organization TEXT       Certificate organization
    --ou TEXT                     Certificate organizational unit
    -s, --state TEXT              Certificate state
    --san TEXT                    Certificate subject alternative name(s) as [TYPE/VALUE,...]
  Logging Parameters:
    --debug                       enable verbose debug output
  -h, --help                      Show this message and exit.
```