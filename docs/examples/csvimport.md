# CSV Import

## Overview

This Python script serves as a command-line tool designed to streamline the process of importing data into an Infoblox
Grid Manager using the Infoblox Web API (WAPI) and CSV files. Users can specify essential parameters such as the Grid
Manager address, the name of the CSV import file, and the desired import operation (**INSERT**, **OVERRIDE**, **MERGE**,
**DELETE**, or **CUSTOM**) when executing the script via the command line. Optional parameters, including username and
WAPI version, provide additional flexibility. The utility also offers debugging capabilities for advanced users. Whether
you need to add, update, or delete data within Infoblox, this script simplifies the import process and offers
customization options to suit your needs.

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

## Example

### CSV Import using Multiple Action

```shell
csvimport -u admin -g 192.168.1.2 -o CUSTOM -f ibcsv_networks.csv 
```

The command invokes the CSV Job Manager and creates a job to import objects using the CUSTOM Operation.

**Screen output from command**

```text
2023-12-09 14:35:20 [nios_csvimport.py:91] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 14:35:20 [fileop.py:243] INFO step 1 - request uploadinit ibcsv_networks.csv
2023-12-09 14:35:20 [fileop.py:266] INFO step 2 - post the files using the upload_url provided
2023-12-09 14:35:20 [fileop.py:276] INFO step 3 - execute the csv_import CUSTOM job on ibcsv_networks.csv
```

**Sample CSV File**

```text
header-network,IMPORT-ACTION,address*,netmask*,dhcp_members,disabled,discovery_member,domain_name,domain_name_servers,network_view,routers
network,O,100.64.50.0,255.255.255.0,ns1.ffy.network,FALSE,nd.ffy.network,ffy.corp,"100.64.50.53,100.64.50.54",default,100.64.50.1
network,O,100.64.40.0,255.255.255.0,,FALSE,nd.ffy.network,,,default,
```

**Importing Multiple Action CSV file**

When you import data, you can include multiple actions, such as add, modify, and delete, in one single CSV file. The
multiple action CSV import file contains multiple types of objects with its headers and data rows listed in the order of
their dependency hierarchy.

The CSV import option supports insert, merge/override and delete operations. To combine these operations together in a
single CSV file, you must specify an optional IMPORT-ACTION column in the CSV import file. The column value for each
data row describes the type of action that the appliance supports for the respective row. The action values include the
following: `I` (Insert), `M` (Merge), `O` (Override), `IM` (Insert + Merge), `IO` (Insert + Override), `D` (Delete).

!!! Note
    You must specify appropriate values in the IMPORT-ACTION column for each row to perform a multiple action CSV
    import. The appliance performs the respective operation when you specify `I`, `M`, `O`, `D`, in the
    IMPORT-ACTION column. When you specify `IM` or `IO`, the appliance first checks if the corresponding object exists. If
    it exists, the appliance performs the merge or override operation accordingly. If the object does not exist, you must
    first perform the insert operation to add the data.

!!! Danger
    CSV imports and operations that involve massive data, such as deleting large zones and recursive deletion of
    networks and all child objects, will significantly affect member performance, resulting in service outage.


    
