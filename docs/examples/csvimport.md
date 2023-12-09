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

## Examples

### CSV Import 

```shell
csvimport -u admin -g 192.168.1.2 -o INSERT -f ibcsv_add_network.csv
```

The command invokes the CSV Job Manager and creates a job to import objects using the INSERT Operation.

```text
csvimport -u admin -g 192.168.1.2 -o INSERT -f ibcsv_add_network.csv
Enter password for [admin]: 
2023-12-09 16:23:07 [nios_csvimport.py:91] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 16:23:07 [fileop.py:243] INFO step 1 - request uploadinit ibcsv_add_network.csv
2023-12-09 16:23:07 [fileop.py:266] INFO step 2 - post the files using the upload_url provided
2023-12-09 16:23:07 [fileop.py:276] INFO step 3 - execute the csv_import INSERT job on ibcsv_add_network.csv

```

**Sample CSV File**
```text
header-network,address*,netmask*,dhcp_members,disabled,domain_name,domain_name_servers,network_view,routers
network,192.168.1.0,255.255.255.0,ns1.ffy.network,FALSE,ffy.corp,"100.64.50.53,100.64.50.54",default,192.168.1.1
```

### CSV Delete

```shell
csvimport -u admin -g 192.168.1.2 -o DELETE -f ibcsv_add_network.csv
```

The command invokes the CSV Job Manager and creates a job to delete objects using the DELETE Operation.

**Screen output from command**

```text
csvimport -u admin -g 192.168.1.2 -o DELETE -f ibcsv_delete_network.csv
Enter password for [admin]: 
2023-12-09 16:23:07 [nios_csvimport.py:91] INFO connected to Infoblox grid manager 192.168.1.2
2023-12-09 16:23:07 [fileop.py:243] INFO step 1 - request uploadinit ibcsv_delete_network.csv
2023-12-09 16:23:07 [fileop.py:266] INFO step 2 - post the files using the upload_url provided
2023-12-09 16:23:07 [fileop.py:276] INFO step 3 - execute the csv_import DELETE job on ibcsv_delete_network.csv

```

**Sample CSV File**
```text
header-network,address*,netmask*
network,192.168.1.0,255.255.255.0
```

### CSV Multiple Action

```shell
csvimport -u admin -g 192.168.1.2 -o CUSTOM -f ibcsv_networks.csv 
```

The command invokes the CSV Job Manager and creates a job to take specific actions for objects using the Multiple Action CUSTOM Operation.

**Screen output from command**

```text
csvimport -u admin -g 192.168.1.2 -o CUSTOM -f ibcsv_network.csv
Enter password for [admin]: 
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
single CSV file, you must specify an optional `IMPORT-ACTION` column in the CSV import file. The column value for each
data row describes the type of action that the appliance supports for the respective row. 

| Action | Description       | Notes                                                                                                                                           |
|--------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| I      | Insert            | If it exists, an error will be generated.                                                                                                       |
| M      | Merge             | If it exists, additional fields will be merged into the record. If the object does not exist, you must first perform the insert operation to add the data.                                 |
| O      | Override          | If it exists, all fields will be overridden. If the object does not exist, you must first perform the insert operation to add the data.                                                                                                   |
| IM     | Insert + Merge    | The appliance first checks if the corresponding object exists. If it exists, the appliance performs the merge or override operation accordingly. |
| IO     | Insert + Override | The appliance first checks if the corresponding object exists. If it exists, the appliance performs the merge or override operation accordingly. |
| D      | Delete            | If it exists, record will be deleted.  If it does not exists, an error will be generated.                                                       |

!!! Danger
    CSV imports and operations that involve massive data, such as deleting large zones and recursive deletion of
    networks and all child objects, will significantly affect member performance, resulting in service outage.

