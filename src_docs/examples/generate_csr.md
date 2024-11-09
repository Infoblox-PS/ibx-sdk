# Generate CSR

## Overview

This program is a command-line utility designed to simplify the process of generating an SSL Certificate Signing
Request or CSR from an Infoblox Grid Manager.

## Usage

To invoke the usage run `generate-csr --help`

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

## Example

### CSV Export

```shell
csvexport -u admin -g 192.168.1.2 -n gm.example.com -m ibxgm.example.com -s 'DNS/ibxgm.example.com,IP/192.168.1.2'
```

The above command will create a CSR or certificate signing request for the member `ibxgm.example.com` with a common
name set to `gm.example.com` the SAN or Subject Alternative Names will include `ibxgm.example.com` and `192.168.1.2`
in the CSR. Once complete, the CSR is downloaded from the grid and saved as `cert.pem`.

**Screen output from command**

```text
Enter password for [admin]:
2024-11-09 15:14:14 [nios_gen_csr.py:152] INFO connected to Infoblox grid manager 192.168.1.2
2024-11-09 15:14:14 [fileop.py:309] INFO generating ADMIN csr for gm.example.com
2024-11-09 15:14:18 [fileop.py:354] INFO downloading data from https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1109221418162387/cert.pem
2024-11-09 15:14:18 [fileop.py:831] INFO https://192.168.1.2/http_direct_file_io/req_id-DOWNLOAD-1109221418162387/cert.pem
2024-11-09 15:14:19 [fileop.py:924] INFO writing file: cert.pem
2024-11-09 15:14:19 [fileop.py:822] INFO file cert.pem download complete
2024-11-09 15:14:19 [nios_gen_csr.py:185] INFO finished!
```
   
