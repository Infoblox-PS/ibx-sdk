# CSV Export

## Overview

This Python program is a command-line utility designed to simplify the process of exporting data from an Infoblox Grid
Manager using the Infoblox Web API (WAPI) and saving it to a CSV file. With this tool, users can specify essential
parameters like the Grid Manager address, the desired output file name, and their authentication credentials.
Additionally, it provides flexibility by allowing users to specify options such as the Infoblox WAPI version and the
type of Infoblox objects to export. Whether you need to extract network information, DNS records, or other data managed
by Infoblox, this utility streamlines the process, making it a valuable resource for Infoblox administrators and users
who need to work with data in CSV format.

## Usage

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

## Examples

```sh
csvexport -u admin -g 192.168.1.2 -f networks.csv -o network
```

```sh
csvexport -u admin -g 192.168.1.2 -f arecs.csv -o record:a
```

```sh
csvexport -u admin -g 192.168.1.2 -f hosts.csv -o record:host
```

```sh
csvexport -u admin -g 192.168.1.2 -f ranges.csv -o range
```

The Infoblox API & CSV Documentation can be found at [https://docs.infoblox.com]().

