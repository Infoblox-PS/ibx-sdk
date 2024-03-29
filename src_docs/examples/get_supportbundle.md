# Get Support Bundle

## Overview

This program is a command-line utility designed to retrieve support-bundles from the Grid.

## Usage

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

### Support Bundle Download

The following example will download the supportbundle with rotated logs and log files from the
infoblox.localdomain.

```sh
get-supportbundle -u admin -g 192.168.1.2 -m infoblox.localdomain -r -l
```

**Screen output from command**

```text
et-supportbundle -g 192.168.1.2 -m ns1.ffy.network -r -l
Enter password for [admin]: 
2023-12-09 19:21:32 [nios_get_supportbundle.py:91] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 19:21:32 [fileop.py:918] INFO performing get_support_bundle for ns1.ffy.network object(s)
2023-12-09 19:22:33 [fileop.py:952] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1210012132961808/supportBundle.tar.gz
2023-12-09 19:22:33 [fileop.py:675] INFO https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1210012132961808/supportBundle.tar.gz
2023-12-09 19:22:33 [fileop.py:41] INFO writing file: 2023120933-infoblox.localdomain-SupportBundle.tgz
2023-12-09 19:22:38 [fileop.py:727] INFO file 2023120933-infoblox.localdomain-SupportBundle.tgz download complete
2023-12-09 19:22:38 [nios_get_supportbundle.py:99] INFO finished!
```
