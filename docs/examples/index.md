# Infoblox Example Tools

We believe that users can simplify their Infoblox Management with these Python Command-Line Utilities.

These tools are a basic powerful suite of Python command-line utilities tailored to enhance the experience with Infoblox
Grid Manager using the Infoblox Web API (WAPI). These tools are designed to cater to the needs of both Infoblox
administrators and users, offering efficient ways to interact with Infoblox data.

**Infoblox NIOS** stands as a robust DDI (DNS, DHCP, and IPAM) platform, and these utilities are here to make various
tasks more accessible, including data manipulation, log retrieval, backup creation, configuration restoration, and
protocol service management. By harnessing the capabilities of these tools, you can streamline your daily Infoblox
operations, making them smoother and more effective.

**Customization**: These tools are highly adaptable and can be tailored to meet specific requirements, ensuring that
they remain versatile for your unique use cases.

Let's delve into each of these tools, understanding their purpose and capabilities:

1. **CSV Export Tool**
    - Export data from Infoblox Grid Manager to CSV format.
    - Define parameters like Grid Manager address, output file name, and authentication credentials.
    - Choose the Infoblox WAPI version and specify the type of data objects to export.
    - [CSV Export Tool Details](csvexport.md)

2. **CSV Import Tool**
    - Import data into Infoblox Grid Manager from CSV files.
    - Configure parameters such as Grid Manager address, import file name, and operation type (INSERT, OVERRIDE, MERGE,
      DELETE, CUSTOM).
    - Fine-tune imports with optional parameters and debugging capabilities.
    - [CSV Import Tool Details](csvimport.md)

3. **Get File Tool**
    - Retrieve configuration files from an Infoblox Grid Manager.
    - Specify the Grid Manager address, target member, and configuration type.
    - Tailor the retrieval process with optional parameters such as admin username and debugging options.
    - [Get File Tool Details](get_file.md)

4. **Get Log Tool**
    - Retrieve logs from an Infoblox Grid Manager, including syslog data.
    - Set parameters for Grid Manager address, target member, log type, and additional customizations.
    - Enable debugging and adapt log retrieval to your specific needs.
    - [Get Log Tool Details](get_log.md)

5. **Get Support Bundle Tool**
    - Assemble a Support Bundle from an Infoblox Grid Manager.
    - Input vital parameters, including Grid Manager address and target member.
    - Add optional parameters such as admin username, log file inclusion, and debugging options.
    - [Get Support Bundle Tool Details](get_supportbundle.md)

6. **Grid Backup Tool**
    - Create backups of an Infoblox NIOS Grid.
    - Specify Grid Manager address and backup file name.
    - Customize the backup process with optional parameters to fit your needs.
    - [Grid Backup Tool Details](grid_backup.md)

7. **Grid Restore Tool**
    - Restore an Infoblox NIOS Grid from a backup.
    - Configure parameters like Grid Manager's IP or hostname, backup filename, restoration mode, and IP configuration
      options.
    - Access debugging capabilities for advanced operations.
    - [Grid Restore Tool Details](grid_restore.md)

8. **Restart Service Tool**
    - Restart Infoblox NIOS Protocol Services.
    - Select the Grid Manager address and the specific service(s) to restart.
    - Further customize with optional parameters and debugging features.
    - [Restart Service Tool Details](restart_service.md)

9. **Service Status Tool**
    - Check the status of Infoblox NIOS Protocol Services.
    - Input essential parameters, such as the Grid Manager's address.
    - Enhance control with optional parameters like admin username and WAPI version.
    - [Service Status Tool Details](restart_status.md)

Each of these tools simplifies a specific aspect of Infoblox management, offering flexibility and customization options
to meet your unique requirements. Whether you're an Infoblox administrator or a user working with Infoblox data, these
utilities will become valuable assets in your daily operations.