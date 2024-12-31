# NIOS SSL Certificate Tool

## Overview

The NIOS SSL Certificate tool `nios-certificate` is a CLI program with several sub-commands
useful for managing SSL Certificates in a NIOS Grid. The tool currently supports the following
commands:

- Download certificate
- Upload certificate
- Generate Certificate Signing Request or CSR
- Generate self-signed certificate

## Usage

The main usage can be invoked by `nios-certificate -h`

```
Usage: nios-certificate [OPTIONS] COMMAND [ARGS]...

  NIOS SSL Certificate Tools

Options:
  -h, --help  Show this message and exit.

Commands:
  download
  gencsr
  selfsign
  upload
```

## Example

### Generate CSR

```shell
nios-certificate gencsr -u admin -g 192.168.1.2 -n gm.example.com -m gm.example.com \
  -s 'DNS/ddi.example.com,IP/192.168.1.2'
```

The above command will create a CSR or certificate signing request for the member
`gm.example.com` with a CN or common name set to `gm.example.com` the SAN or Subject Alternative 
Names will include `ddi.example.com` and `192.168.1.2` in the CSR. Once complete, the CSR is 
downloaded from the grid and saved as `cert.pem`.

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
   
