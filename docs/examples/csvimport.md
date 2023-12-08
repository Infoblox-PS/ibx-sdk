# CSV Import

## Overview

This Python script serves as a command-line tool designed to streamline the process of importing data into an Infoblox
Grid Manager using the Infoblox Web API (WAPI) and CSV files. Users can specify essential parameters such as the Grid
Manager address, the name of the CSV import file, and the desired import operation (INSERT, OVERRIDE, MERGE, DELETE, or
CUSTOM) when executing the script via the command line. Optional parameters, including username and WAPI version,
provide additional flexibility. The utility also offers debugging capabilities for advanced users. Whether you need to
add, update, or delete data within Infoblox, this script simplifies the import process and offers customization options
to suit your needs.

## Usage

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

## Examples

```sh
csvimport -u admin -g 192.168.1.2 -f networks.csv -o INSERT
```

```sh
csvimport -u admin -g 192.168.1.2 -f ranges.csv -o DELETE
```

The Infoblox API & CSV Documentation can be found at [https://docs.infoblox.com]().