"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from typing import Optional, Union, Literal

import requests
import urllib3
from requests import Response

from ibx_tools.nios import fileop
from ibx_tools.nios import service

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ServiceRestartOption = Literal['FORCE_RESTART', 'RESTART_IF_NEEDED']
ServiceRestartServices = Literal['ALL', 'DNS', 'DHCP', 'DHCPV4', 'DHCPV6']
ServiceRestartMode = Literal['GROUPED', 'SEQUENTIAL', 'SIMULTANEOUS']
CsvOperation = Literal['INSERT', 'UPDATE', 'DELETE', 'REPLACE', 'MERGE', 'OVERRIDE', 'CUSTOM']
GridRestoreMode = Literal['NORMAL', 'FORCED', 'CLONE']
MemberDataType = Literal[
    'DNS_CACHE',
    'DNS_CFG',
    'DHCP_CFG',
    'DHCPV6_CFG',
    'TRAFFIC_CAPTURE_FILE',
    'DNS_STATS',
    'DNS_RECURSING_CACHE'
]
LogType = Literal['SYSLOG', 'AUDIT_LOG', 'MSMGMTLOG', 'DELTALOG', 'OUTBOUND', 'PTOPLOG', 'DISCOVERY_CSV_ERRLOG']


class BaseWapiException(Exception):
    """BaseWapiException class"""


class WapiRequestException(BaseWapiException):
    """WapiRequestException class - returns error(s) returned from Infoblox WAPI calls"""

    def __init__(self, msg):
        super().__init__(
            f'wapi error - {msg}'
        )


class WAPI(requests.sessions.Session):
    """Handles interactions with the Infoblox WAPI.

    This class provides a range of classes to interact with Infoblox WAPI,
    including session management, data retrieval, file operations, and service management.

    Attributes:
        grid_mgr (str): IP address or hostname of the Grid Manager.
        username (str): Username for authentication with the Infoblox WAPI.
        password (str): Password for authentication.
        wapi_ver (str): Version of the Infoblox WAPI.
        ssl_verify (bool): Flag to determine SSL certificate verification.
        conn (requests.sessions.Session, optional): Active session to the WAPI grid. Default is None.
        grid_ref (str, optional): Reference ID of the connected grid. Default is None.

    Examples:

    Initialize the WAPI instance with a dictionary of properties:

    ```py

    wapi_properties = {
        'grid_mgr': 'gm.example.com',
        'username': 'admin',
        'password': 'infoblox',
        'wapi_ver': '2.11',
        'ssl_verify': False
    }
    wapi = WAPI(wapi_properties)

    wapi.connect()

    ```

    Build up the WAPI instance one property at a time:

    ```python

    wapi = WAPI()

    wapi.grid_mgr = 'gm.example.com'
    wapi.username = 'admin'
    wapi.password = 'infoblox'
    wapi.wapi_ver = '2.11'
    wapi.ssl_verify = False

    wapi.connect()

    ```
    """

    def __init__(
            self,
            grid_mgr: str = None,
            username: str = 'admin',
            password: str = 'infoblox',
            wapi_ver: str = '2.5',
            ssl_verify: bool = False) -> None:
        super().__init__()
        self.grid_mgr = grid_mgr
        self.username = username
        self.password = password
        self.wapi_ver = wapi_ver
        self.ssl_verify = ssl_verify
        self.conn = None
        self.grid_ref = None

    def __repr__(self):
        args = []
        for key, value in self.__dict__.items():
            if key == 'password':
                value = '*******'
            args.append(f'{key}={value}')
        return f"{self.__class__.__qualname__}({', '.join(args)})"

    @property
    def url(self) -> str:
        """
        Constructs a property using `grid_mgr` and `wapi_ver` attributes for the WAPI class.

        Parameters:
        - grid_mgr (str): The IP address or hostname of the grid manager.
        - wapi_ver (str): The version of the WAPI.

        Returns:
        - url (str): The URL constructed using the grid manager and WAPI version.

        Raises:
        - None.

        Example:

        ```python

        wapi = WAPI()
        wapi.grid_mgr = '10.0.0.1'
        wapi.wapi_ver = '2.10'
        url = wapi.url

        print(url)

        ```
        The above code example will return output:

        ```
        'https://10.0.0.1/wapi/v2.10'
        ```

        """
        if self.grid_mgr and self.wapi_ver:
            return f'https://{self.grid_mgr}/wapi/v{self.wapi_ver}'
        return ''

    def object_fields(self, wapi_object: str) -> Union[str, None]:
        """
        Retrieves the object fields for a specified WAPI object.

        Args:
            wapi_object (str): The name of the WAPI object for which to retrieve the fields.

        Returns:
            Union[str, None]: A string containing the fields separated by commas, or None if an error occurred.

        Raises:
            WapiRequestException: If there was an error connecting to the WAPI service.

        Example:

        ```py
        wapi = WAPI()
        fields = wapi.object_fields('record:host')
        if fields is not None:
            print(f"Fields: {fields}")
        ```
        """
        try:
            logging.debug('trying %s/%s?_schema', self.url, wapi_object)
            res = self.conn.get(f'{self.url}/{wapi_object}?_schema', verify=self.ssl_verify)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err) from err
        else:
            fields = ",".join(field["name"] for field in data.get('fields') if "r" in field.get('supports'))
        return fields

    def max_wapi_ver(self) -> None:
        """
        Retrieves the maximum supported version of the WAPI.

        Returns:
            None

        Raises:
            WapiRequestException: If there is an error making the GET request to retrieve the WAPI version.

        Example Usage:

        ```py
        session = WAPI()
        session.max_wapi_ver()
        print(session.wapi_ver)  # Prints the maximum supported WAPI version
        ```

        """
        url = f'https://{self.grid_mgr}/wapi/v1.0/?_schema'
        try:
            logging.debug('trying %s', url)
            res = self.conn.get(url, verify=False)
            res.raise_for_status()
            data = res.json()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err) from err
        else:
            versions = data.get('supported_versions')
            versions.sort(key=lambda s: list(map(int, s.split('.'))))
            logging.debug(versions)
            max_wapi_ver = versions.pop()
            setattr(self, 'wapi_ver', max_wapi_ver)

    def connect(self) -> None:
        """
        Connects to the WAPI grid.

        Raises:
            WapiRequestException: If there is an error in making the request to the WAPI grid.

        Returns:
            None: Returns nothing.

        """
        if not self.url:
            logging.error('invalid url %s - unable to connect!', self.url)
            return

        with requests.sessions.Session() as conn:
            try:
                res = conn.get(
                    f'{self.url}/grid',
                    auth=(self.username, self.password),
                    verify=self.ssl_verify
                )
                res.raise_for_status()
                grid = res.json()
            except requests.exceptions.RequestException as err:
                logging.error(err)
                raise WapiRequestException(err) from err
            else:
                setattr(self, 'conn', conn)
                setattr(self, 'grid_ref', grid[0].get('_ref'))
                return

    def get(self, url, params=None, **kwargs) -> Response:
        """
        This method performs a GET request to the specified URL.

        Args:
            url: The URL to which the GET request will be sent.
            params: Optional parameters to be passed in the request URL.
            **kwargs: Additional keyword arguments to be passed to the underlying `requests.Session.request` method.

        Returns:
            A `requests.Response` object containing the server's response to the GET request.

        """
        return self.conn.request('get', url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        """
        Send a POST request to the supplied URL

        Args:
            url: The URL to which the POST request will be sent.
            data: Optional. The data to be sent in the body of the request.
            json: Optional. The JSON data to be sent in the body of the request.
            **kwargs: Optional keyword arguments.

        """
        return self.conn.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> Response:
        """
        Performs a PUT request to the specified URL with the provided data. Additional parameters can be passed
        through the **kwargs argument.

        Args:
            url: The URL to send the PUT request to.
            data: The data to include in the PUT request, if any.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            A Response object representing the server's response to the PUT request.

        Example usage:

        ```py
        wapi = WAPI()
        response = wapi.put('https://example.com/api/resource/123', data={'name': 'John Doe'})
        if response.status_code == 200:
            print('PUT request successful.')
        else:
            print('PUT request failed with status code: {}'.format(response.status_code)
        ```
        """
        return self.conn.request('delete', url, **kwargs)

    def member_config(self, member: str, conf_type: MemberDataType, remote_url: str = None) -> str:
        """
        Fetch a Grid Member's DNS or DHCP config file

        Args:
            member (str): The name or IP address of the member.
            conf_type (MemberDataType): The type of configuration file to download.
            remote_url (str, optional): The remote URL from which to download the configuration file. Defaults to None.

        Returns:
            str: The path of the downloaded configuration file.

        """
        return fileop.member_config(self, member, conf_type, remote_url)

    def csv_export(self, wapi_object: str, filename: Optional[str] = None) -> None:
        """
        Export data from the WAPI to a CSV file.

        Args:
            wapi_object (str): The WAPI object to export data from.
            filename (Optional[str]): The name of the CSV file to export the data to. If not provided,
                the data will be exported to a default file.

        Raises:
            None

        Returns:
            None
        """
        fileop.csv_export(self, wapi_object, filename)

    def csv_import(
            self,
            task_operation: CsvOperation,
            csv_import_file: str,
            exit_on_error: bool = False) -> dict:
        """
        Imports a CSV file into the Infoblox WAPI.

        Args:
            task_operation (CsvOperation): The operation to perform on the CSV file.
            csv_import_file (str): The path to the CSV file to import.
            exit_on_error (bool, optional): Whether to exit on error. Defaults to False.

        Returns:
            dict: The response from the CSV import task.
        """
        return fileop.csv_import(self, task_operation, csv_import_file, exit_on_error)

    def grid_restore(
            self,
            filename: str = "database.tgz",
            mode: GridRestoreMode = "NORMAL",
            keep_grid_ip: bool = False):
        """
        Restores the Infoblox grid database from a backup file.

        Args:
            self: The current instance of the WAPI class.
            filename (str): The name of the backup file to restore. Defaults to "database.tgz".
            mode (str): The restore mode. Defaults to "NORMAL".
            keep_grid_ip (bool): Boolean flag to indicate whether to keep the grid IP address. Defaults to False.

        Returns:
            None

        Raises:
            None

        Example:

        ```py
        wapi = WAPI()
        wapi.grid_restore(filename="database.tgz", mode="NORMAL", keep_grid_ip=True)
        ```
        :rtype: object
        """
        fileop.grid_restore(self, filename, mode, keep_grid_ip)

    def grid_backup(self, filename: str = "database.tgz"):
        """
        Perform a NIOS Grid Backup

        Args:
            filename (str): The name of the backup file. Defaults to "database.tgz".

        Returns:
            None

        Description:
        This method is used to initiate a grid backup in the Infoblox NIOS WAPI. It makes use of the
        fileop.grid_backup() method from the infoblox_pslib.nios.fileop module. The backup is saved with the
        specified filename in the Infoblox Grid.

        Example:

        ```py
        session = WAPI()
        session.grid_backup(filename="backup_file.tgz")
        ```

        This will initiate a grid backup with the provided filename "backup_file.tgz".
        """
        fileop.grid_backup(self, filename)

    def get_service_restart_status(self) -> dict:
        """
            Retrieves the restart status of a service through the Infoblox WAPI.

            Args:
                self: The WAPI session object.

            Returns:
                Optional[Union[str, bool]]: The restart status of the service.
                It returns None if the service restart status is not available or
                if there was an error retrieving the restart status.

            Raises:
                None.

        """
        return service.get_service_restart_status(self)

    def service_restart(
            self,
            groups: Optional[list] = None,
            members: Optional[list[str]] = None,
            mode: Optional[ServiceRestartMode] = None,
            restart_option: Optional[ServiceRestartOption] = 'RESTART_IF_NEEDED',
            services: Optional[list[ServiceRestartServices]] = None,
            user_name: Optional[str] = None,
    ):
        """
        Restarts services on Infoblox appliances.

        Args:
            groups (Optional[list]): List of group names containing appliances. Default is None.
            members (Optional[list[str]]): List of member names within the given groups. Default is None.
            mode (Optional[ServiceRestartMode]): Service restart mode. Default is None.
            restart_option (Optional[ServiceRestartOption]): Service restart option. Default is 'RESTART_IF_NEEDED'.
            services (Optional[list[ServiceRestartServices]]): List of member services to restart. Default is
            'ALL'.
            user_name (Optional[str]): Username for authentication. Default is None.

        """
        service.service_restart(
            self,
            groups=groups,
            members=members,
            mode=mode,
            restart_option=restart_option,
            services=services,
            user_name=user_name
        )

    def csv_task_status(self, csvtask: dict) -> dict:
        """
        fetch the CSV task status of a CSV import task

        Args:
            csvtask: A dictionary representing the csv task.

        Returns:
            A dictionary containing the status of the csv task.

        Raises:
            None.
        """
        return fileop.csvtask_status(self, csvtask=csvtask)

    def get_csv_errors_file(self, filename: str, job_id: str) -> None:
        """
        fetch the CSV Errors file of a CSV task

        Args:
            filename (str): The name of the CSV errors file.
            job_id (str): The ID of the job that generated the CSV errors file.

        """
        return fileop.get_csv_errors_file(self, filename=filename, job_id=job_id)

    def get_support_bundle(
            self,
            member: str,
            cached_zone_data: bool = False,
            core_files: bool = False,
            log_files: bool = False,
            nm_snmp_logs: bool = False,
            recursive_cache_file: bool = False,
            remote_url: Optional[str] = None,
            rotate_log_files: bool = False
    ):
        """
        fetch a support bundle from the specified Grid Member

        Args:
            member (str): The name or IP address of the target member.
            cached_zone_data (bool): Whether to include cached zone data in the support bundle. Default is False.
            core_files (bool): Whether to include core files in the support bundle. Default is False.
            log_files (bool): Whether to include log files in the support bundle. Default is False.
            nm_snmp_logs (bool): Whether to include NIOS Maintenance SNMP logs in the support bundle. Default is False.
            recursive_cache_file (bool): Whether to recursively include the cache in the support bundle. Default is
            False.
            remote_url (str, optional): The URL of a remote server to upload the support bundle to. Default is None.
            rotate_log_files (bool): Whether to rotate log files after creating the support bundle. Default is False.

        Returns:
            Response: The response object containing the result of the support bundle creation request.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the support bundle creation request.
        """
        return fileop.get_support_bundle(
            self,
            member=member,
            cached_zone_data=cached_zone_data,
            core_files=core_files,
            log_files=log_files,
            nm_snmp_logs=nm_snmp_logs,
            recursive_cache_file=recursive_cache_file,
            remote_url=remote_url,
            rotate_log_files=rotate_log_files
        )

    def get_log_files(
            self,
            log_type: LogType,
            endpoint: Optional[str] = None,
            include_rotated: bool = False,
            member: Optional[str] = None,
            msserver: Optional[str] = None,
            node_type: Optional[Literal['ACTIVE', 'BACKUP']] = None
    ):
        """
        Fetches the log(s) from NIOS for given log_type

        Args:
            log_type: The type of log files to retrieve. Accepted values are 'debug', 'query', 'dhcp', 'dns',
            'auto_discovery', 'event', 'object_management', 'reporting', 'file_integration', 'traffic_management',
            'threat_insight', 'cloud_network', 'external_dns', 'external_autodiscover', and 'external_forwarding'.
            endpoint: The endpoint IP address or hostname for which to retrieve the log files.
            include_rotated: Whether to include rotated log files. Defaults to False.
            member: The member name for which to retrieve the log files.
            msserver: The Microsoft Windows server IP address or hostname for which to retrieve the log files.
            node_type: The node type of the appliance for which to retrieve the log files. Accepted values are
            'ACTIVE' and 'BACKUP'.

        Returns:
            The response object containing the log files.

        """
        return fileop.get_log_files(
            self,
            log_type=log_type,
            endpoint=endpoint,
            include_rotated=include_rotated,
            member=member,
            msserver=msserver,
            node_type=node_type
        )
