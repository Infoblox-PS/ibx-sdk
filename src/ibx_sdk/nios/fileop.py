"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import os
import pprint
from typing import Literal, Optional

import requests.exceptions

from ibx_sdk.nios.exceptions import WapiRequestException
from ibx_sdk.util import util

CsvOperation = Literal[
    "INSERT", "UPDATE", "DELETE", "REPLACE", "MERGE", "OVERRIDE", "CUSTOM"
]
GridRestoreMode = Literal["NORMAL", "FORCED", "CLONE"]
SupportedAlgorithms = Literal["SHA-1", "SHA-256", "SHA-384", "SHA-512"]
SupportedKeySizes = Literal[1024, 2048, 4096]
SupportedCertUsages = Literal["ADMIN", "CAPTIVE_PORTAL", "SFNT_CLIENT_CERT", "IFMAP_DHCP"]
SupportedCertTypes = Literal["ADMIN", "CAPTIVE_PORTAL", "SFNT_CLIENT_CERT", "IFMAP_DHCP", "EAP_CA", "TAE_CA"]
LogType = Literal[
    "SYSLOG",
    "AUDITLOG",
    "MSMGMTLOG",
    "DELTALOG",
    "OUTBOUND",
    "PTOPLOG",
    "DISCOVERY_CSV_ERRLOG",
]
MemberDataType = Literal[
    "DNS_CACHE",
    "DNS_CFG",
    "DHCP_CFG",
    "DHCPV6_CFG",
    "TRAFFIC_CAPTURE_FILE",
    "DNS_STATS",
    "DNS_RECURSING_CACHE",
]


class NiosFileopMixin:
    """
    NiosFileopMixin class
    """

    def csv_export(self, wapi_object: str, filename: Optional[str] = None) -> None:
        """
        Perform a NIOS CSV Export Task for a given WAPI object

        Args:
            wapi_object: The name of the WAPI object to perform a CSV export on.
            filename: Optional. The name of the file to save the exported data to. If not
                                provided, a default filename will be generated based on the
                                download URL.

        Raises:
            requests.exceptions.RequestException: If there is an error in the request.

        Returns:
            None

        """
        if filename:
            (_, filename) = os.path.split(filename)
            filename = os.path.join(_, filename.replace("-", "_"))

        # Call WAPI fileop  csv_export function
        logging.info("performing csv export for %s object(s)", wapi_object)
        payload = {"_object": wapi_object}
        try:
            response = self.post(
                "fileop", params={"_function": "csv_export"}, json=payload
            )
            logging.debug(response.text)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = response.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        logging.info("downloading data from %s", download_url)
        response = self.__download_file(download_url, self.__get_cookies())

        if not filename:
            filename = util.extract_filename_from_url(download_url)

        NiosFileopMixin.__write_file(filename=filename, data=response)

        self.__download_complete(download_token, filename, self.__get_cookies())

    def file_download(
            self,
            token: str,
            url: str,
            filename: str = None,
    ) -> None:
        """
        file_download downloads the generated file from the NIOS Grid using a token and url

        Args:
            token: Authentication token required for the download completion.
            url: URL of the file to be downloaded.
            filename: Optional; name for the downloaded file. If not provided, it will be extracted from the URL.

        Returns:
            None
        """
        logging.info("downloading data from %s", url)
        try:
            res = self.__download_file(url, self.__get_cookies())
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        if not filename:
            filename = util.extract_filename_from_url(url)

        NiosFileopMixin.__write_file(filename=filename, data=res)

        try:
            self.__download_complete(token, filename, self.__get_cookies())
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

    def file_upload(self, filename: str) -> str:
        """
        Perform a file upload into the NIOS Grid.

        Args:
            filename: The path of the file to be uploaded.

        Returns:
            str: The token received upon successful upload initialization.

        Raises:
            WapiRequestException: If there is a request exception during the upload process.
        """
        (path, filename) = os.path.split(filename)
        valid_filename = filename.replace("-", "_")

        # Call WAPI fileop Upload INIT
        logging.info("step 1 - request uploadinit %s", filename)
        try:
            obj = self.__upload_init(filename=valid_filename)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        upload_url = obj.get("url")
        token = obj.get("token")

        # specify a file handle for the file data to be uploaded
        with open(os.path.join(path, filename), "rb") as fh:
            # reset to top of the file
            fh.seek(0)
            upload_file = {"file": fh.read()}

            # Upload the contents of the CSV file
            logging.info("step 2 - post the files using the upload_url provided")
            try:
                self.__upload_file(upload_url, upload_file, self.__get_cookies())
            except requests.exceptions.RequestException as err:
                logging.error(err)
                raise WapiRequestException(err)
            else:
                return token

    def upload_certificate(
            self,
            member: str,
            filename: str,
            certificate_usage: SupportedCertTypes = "ADMIN",
    ):
        """
        Upload an SSL Certificate file to the Grid

        Args:
            member: The member identifier to which the certificate will be uploaded.
            filename: The filename of the certificate to be uploaded.
            certificate_usage: The usage type of the certificate. Default is "ADMIN".

        Raises:
            WapiRequestException: If there is an error during the request to upload the certificate.
        """
        token = self.file_upload(filename=filename)

        # submit task to CSV Job Manager
        logging.info("step 3 - upload %s certificate on %s", certificate_usage, member)
        payload = {"certificate_usage": certificate_usage, "member": member, "token": token}
        try:
            res = self.post(
                "fileop",
                params={"_function": "uploadcertificate"},
                json=payload,
                cookies=self.__get_cookies(),
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

    def csv_import(
            self,
            task_operation: CsvOperation,
            csv_import_file: str,
            exit_on_error: bool = False,
    ) -> dict:
        """
        Perform a CSV import task using the NIOS CSV Task Manager

        Args:
            task_operation (CsvOperation): The operation to be performed on the CSV file. Should be
                                           a value from the `CsvOperation` enum.
            csv_import_file (str): The path to the CSV file to be imported.
            exit_on_error (bool): Indicates whether the program should exit if an error occurs
                                  during the import process. Default value is `False`.

        Returns:
            A dictionary containing the result of the CSV import task.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making HTTP requests.
        """
        token = self.file_upload(filename=csv_import_file)

        # submit task to CSV Job Manager
        logging.info(
            "step 3 - execute the csv_import %s job on %s",
            task_operation,
            csv_import_file,
        )
        try:
            csvtask = self.__csv_import(
                task_operation.upper(), token, self.__get_cookies(), exit_on_error
            )
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)
        else:
            return csvtask

    def csvtask_status(self, csvtask: dict) -> dict:
        """
        Fetch the status of a CSV submitted task

        Args:
            csvtask (dict): The dictionary containing the information about the CSV import task.

        Returns:
            dict: The JSON response containing the status of the CSV import task.

        Raises:
            RequestException: If there is an error in the request.

        Description:
            This method is used to check the status of a CSV import task. It takes a dictionary,
            `csvtask`, as input, which contains the information about the CSV import task. The
            `csvtask` dictionary should have the following structure:

            {
                'csv_import_task': {
                    '_ref': '<CSV import task reference>'
                }
            }

            The method first retrieves the `_ref` value from the `csvtask` dictionary to identify
            the import task. It then sends a request to retrieve the status of the import task
            using the `get` method.

            If the status request is successful, the JSON response containing the status is
            logged using the `debug` level.

            Finally, the method returns the JSON response containing the status of the CSV import
            task.

            If there is any error in the request, a `RequestException` is raised and logged using
            the `error` level.

        Example usage:

        ```python
        csvtask = {
            'csv_import_task': {
                '_ref': '12345678'
            }
        }
        status = csvtask_status(csvtask)
        ```
        """
        _ref = csvtask["csv_import_task"]["_ref"]
        logging.debug("Checking status of csvimporttask %s", _ref)
        try:
            res = self.get(_ref)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)
        else:
            logging.debug(res.json())

        return res.json()

    def get_csv_errors_file(self, filename: str, job_id: str) -> None:
        """
        Fetches the csv-errors file for a specific job ID.

        Args:
            filename (str): The filename to be used when saving the csv-errors file.
            job_id (str): The job ID for which the csv-errors file should be fetched.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If there is an error during the request.

        """
        logging.debug("fetching csv-errors file for job id %s", job_id)
        payload = {"import_id": job_id}
        try:
            res = self.post(
                "fileop", params={"_function": "csv_error_log"}, json=payload
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        token = obj.get("token")
        download_url = obj.get("url")

        try:
            res = self.__download_file(download_url, self.__get_cookies())
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        csv_error_file = f"csv-errors-{filename}.csv"
        NiosFileopMixin.__write_file(filename=csv_error_file, data=res)

        # We're done - so post to downloadcomplete function
        try:
            self.__download_complete(token, csv_error_file, self.__get_cookies())
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

    def download_certificate(
            self,
            member: str,
            certificate_usage: SupportedCertTypes = "ADMIN",
    ):
        """
        Download SSL certificate from the Grid.

        Args:
            member: The identifier of the member for whom the certificate is being downloaded.
            certificate_usage: The type of certificate to be downloaded (e.g., "ADMIN").
        """
        logging.info("Downloading %s certificate for %s", certificate_usage, member)
        payload = {"member": member, "certificate_usage": certificate_usage}
        logging.debug("json payload %s", payload)

        try:
            res = self.post("fileop", params={"_function": "downloadcertificate"}, json=payload)
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url)

    def generate_selfsigned_cert(
            self,
            cn: str,
            member: str,
            days_valid: int = 365,
            algorithm: SupportedAlgorithms = "SHA-256",
            certificate_usage: SupportedCertUsages = "ADMIN",
            comment: Optional[str] = None,
            country: Optional[str] = None,
            email: Optional[str] = None,
            key_size: Optional[SupportedKeySizes] = 2048,
            locality: Optional[str] = None,
            org: Optional[str] = None,
            org_unit: Optional[str] = None,
            state: Optional[str] = None,
            subject_alternative_names: Optional[list[dict]] = None
    ):
        """
        Generate a Self-Signed Certificate on the Grid.

        Args:
            cn: The common name for the certificate.
            member: The member name for the certificate.
            days_valid: The number of days the certificate is valid for. Default is 365.
            algorithm: The algorithm used for certificate generation. Default is "SHA-256".
            certificate_usage: The usage type of the certificate. Default is "ADMIN".
            comment: Optional comment associated with the certificate.
            country: Optional country code.
            email: Optional email address.
            key_size: The size of the key used in certificate generation. Default is 2048.
            locality: Optional locality (e.g., city).
            org: Optional organization name.
            org_unit: Optional organizational unit.
            state: Optional state or province.
            subject_alternative_names: Optional list of subject alternative names.

        """
        logging.info("generating self-signed certificate for %s", member)
        payload = {
            "cn": cn,
            "member": member,
            "algorithm": algorithm,
            "certificate_usage": certificate_usage,
            "days_valid": days_valid,
        }
        if comment:
            payload["comment"] = comment
        if country:
            payload["country"] = country
        if email:
            payload["email"] = email
        if key_size:
            payload["key_size"] = key_size
        if locality:
            payload["locality"] = locality
        if org:
            payload["org"] = org
        if org_unit:
            payload["org_unit"] = org_unit
        if state:
            payload["state"] = state
        if subject_alternative_names:
            payload["subject_alternative_names"] = subject_alternative_names
        logging.debug("json payload %s", payload)

        try:
            res = self.post(
                "fileop", params={"_function": "generateselfsignedcert"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url)

    def generate_csr(
            self,
            cn: str,
            member: str,
            algorithm: SupportedAlgorithms = "SHA-256",
            certificate_usage: SupportedCertUsages = "ADMIN",
            comment: Optional[str] = None,
            country: Optional[str] = None,
            email: Optional[str] = None,
            key_size: Optional[SupportedKeySizes] = 2048,
            locality: Optional[str] = None,
            org: Optional[str] = None,
            org_unit: Optional[str] = None,
            state: Optional[str] = None,
            subject_alternative_names: Optional[list[dict]] = None
    ) -> None:
        """
        Generate a Certificate Signing Request

        Generate and download a CSR for a member of the grid. Once the CSR is generated it is downloaded and saved
        locally to the current working directory.

        Args:
            cn: Common Name for the certificate.
            member: The member for which the certificate is being generated.
            algorithm: Algorithm used for certificate generation, default is "SHA-256".
            certificate_usage: Purpose of the certificate, default is "ADMIN".
            comment: Optional comment for the certificate.
            country: Optional country code for the certificate.
            email: Optional email address for the certificate.
            key_size: Optional key size for the certificate, default is 2048.
            locality: Optional locality or city for the certificate.
            org: Optional organization name for the certificate.
            org_unit: Optional organizational unit for the certificate.
            state: Optional state or province for the certificate.
            subject_alternative_names: Optional list of subject alternative names (SANs) for the certificate.

        Returns:
            None
        """
        logging.info("generating %s csr for %s", certificate_usage, member)
        payload = {
            "cn": cn,
            "member": member,
            "algorithm": algorithm,
            "certificate_usage": certificate_usage,
        }
        if comment:
            payload["comment"] = comment
        if country:
            payload["country"] = country
        if email:
            payload["email"] = email
        if key_size:
            payload["key_size"] = key_size
        if locality:
            payload["locality"] = locality
        if org:
            payload["org"] = org
        if org_unit:
            payload["org_unit"] = org_unit
        if state:
            payload["state"] = state
        if subject_alternative_names:
            payload["subject_alternative_names"] = subject_alternative_names
        logging.debug("json payload %s", payload)

        try:
            res = self.post(
                "fileop", params={"_function": "generatecsr"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url)

    def get_log_files(
            self,
            log_type: LogType,
            filename: Optional[str] = None,
            endpoint: Optional[str] = None,
            include_rotated: bool = False,
            member: Optional[str] = None,
            msserver: Optional[str] = None,
            node_type: Optional[Literal["ACTIVE", "BACKUP"]] = None,
    ):
        """
        Fetch the log files for the provided member or msserver

        Args:
            log_type (LogType): The type of log files to fetch.
            filename (str): The name of the log file to download (Default value = None)
            endpoint (str): The specific endpoint for which to fetch log files. (Default: None)
            include_rotated (bool): Whether to include rotated log files. (Default: False)
            member (str): The member for which to fetch log files. (Default: None)
            msserver (str): The msserver for which to fetch log files. (Default: None)
            node_type: The type of node for which to fetch log files. Can be 'ACTIVE' or
                       'BACKUP'. (Default: None)
        """
        logging.info("fetching %s log files for %s", log_type, member)
        payload = {"log_type": log_type, "include_rotated": include_rotated}

        if endpoint:
            payload["endpoint"] = endpoint
        if member:
            payload["member"] = member
        if node_type:
            payload["node_type"] = node_type
        if msserver:
            payload["msserver"] = msserver

        logging.debug("json payload %s", payload)

        try:
            res = self.post(
                "fileop", params={"_function": "get_log_files"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url, filename=filename)

    def get_support_bundle(
            self,
            member: str,
            filename: Optional[str] = None,
            cached_zone_data: bool = False,
            core_files: bool = False,
            log_files: bool = False,
            nm_snmp_logs: bool = False,
            recursive_cache_file: bool = False,
            remote_url: Optional[str] = None,
            rotate_log_files: bool = False,
    ):
        """
        Get the support bundle for a member.

        Args:
            member (str): The member for which to retrieve the support bundle.
            filename (str, optional): The filename of the support bundle.
            cached_zone_data (bool, optional): Whether to include cached zone data in the support
                                               bundle. Defaults to False.
            core_files (bool, optional): Whether to include core files in the support bundle.
                                         Defaults to False.
            log_files (bool, optional): Whether to include log files in the support bundle.
                                        Defaults to False.
            nm_snmp_logs (bool, optional): Whether to include NM SNMP logs in the support bundle.
                                           Defaults to False.
            recursive_cache_file (bool, optional): Whether to include recursive cache file in the
                                                   support bundle. Defaults to False.
            remote_url (str, optional): The remote URL where the support bundle will be uploaded.
                                        Defaults to None.
            rotate_log_files (bool, optional): Whether to rotate log files before creating the
                                               support bundle. Defaults to False.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the request.

        """
        logging.info("performing get_support_bundle for %s object(s)", member)
        payload = {
            "member": member,
            "cached_zone_data": cached_zone_data,
            "core_files": core_files,
            "log_files": log_files,
            "nm_snmp_logs": nm_snmp_logs,
            "recursive_cache_file": recursive_cache_file,
            "rotate_log_files": rotate_log_files,
        }
        if remote_url:
            payload["remote_url"] = remote_url
        logging.debug(pprint.pformat(payload))
        try:
            res = self.post(
                "fileop", params={"_function": "get_support_bundle"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url, filename=filename)

    def grid_backup(self, filename: Optional[str] = None) -> None:
        """
        Perform a NIOS Grid Backup.

        Args:
            filename: str, optional. The name of the backup file. Default is 'database.bak'.

        Returns:
            None

        Raises:
            requests.exceptions.RequestException: If an error occurs during the backup process.
        """
        payload = {"type": "BACKUP"}

        logging.info("step 1 - request gridbackup %s", filename)
        try:
            res = self.__getgriddata(payload, self.__get_cookies())
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        token = res.get("token")
        download_url = res.get("url")

        logging.info("step 2 - saving backup to %s", filename)
        self.file_download(token=token, url=download_url, filename=filename)

    def grid_restore(
            self,
            filename: str = "database.bak",
            mode: GridRestoreMode = "NORMAL",
            keep_grid_ip: bool = False,
    ):
        """
        Perform a NIOS Grid restore of a database using a given file.

        Args:
            filename (str): The filename of the database file to be restored. Default is
                            "database.bak".
            mode (GridRestoreMode): The restore mode to be used. Default is "NORMAL".
            keep_grid_ip (bool): Indicates whether to keep the grid IP address. Default is False.

        """
        token = self.file_upload(filename=filename)

        # Execute the restore
        logging.info("step 3 - execute the grid restore")
        try:
            self.__restore_database(keep_grid_ip, mode, token, self.__get_cookies())
        except requests.exceptions.RequestException as err:
            logging.error("step 3 - Error: %s", err)
            raise WapiRequestException(err)
        logging.info("Grid restore successful!")

    def member_config(
            self,
            member: str,
            conf_type: MemberDataType,
            filename: Optional[str] = None,
            remote_url: str = None,
    ) -> None:
        """
        Fetch member configuration file for given service type.

        Args:
            member: A string representing the grid member.
            conf_type: An enum representing the type of config file.
            filename: A string value of the filename to save
            remote_url: An optional string representing the remote URL.

        Returns:
            A string representing the downloaded file.

        """
        conf_type = conf_type.upper()
        logging.info("fetching %s config file for grid member %s", conf_type, member)
        payload = {"member": member, "type": conf_type}
        if remote_url:
            payload["remote_url"] = remote_url
        try:
            res = self.post(
                "fileop", params={"_function": "getmemberdata"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url, filename=filename)

    def get_lease_history(
            self,
            member: str,
            start_time: int = None,
            end_time: int = None,
            remove_url: str = None
    ) -> None:
        """
        fetch DHCP lease history files from a NIOS Grid Member

        Args:
            member: A string representing the grid member that the DHCP lease history is being fetched from.
            start_time: An optional integer representing the start time in epoch format. Defaults to None.
            end_time: An optional integer representing the end time in epoch format. Defaults to None.
            remove_url: An optional string representing the remove URL. Defaults to None.

        Returns:
            A string representing the filename of the downloaded DHCP lease history file.

        Raises:
            WapiRequestException: If there is an error in the API request.

        """
        logging.info("fetching DHCP lease history from grid member %s", member)
        payload = {"member": member}
        if start_time is not None:
            payload["start_time"] = start_time
        if end_time is not None:
            payload["end_time"] = end_time
        if remove_url is not None:
            payload["remove_url"] = remove_url
        try:
            res = self.post(
                "fileop", params={"_function": "getleasehistoryfiles"}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        obj = res.json()
        download_url = obj.get("url")
        download_token = obj.get("token")

        self.file_download(token=download_token, url=download_url)

    def __csv_import(
            self,
            task_operation: str,
            upload_token: str,
            req_cookies: dict,
            exit_on_error: bool = False,
    ) -> dict:
        headers = {"content-type": "application/json"}

        # set the request parameters
        payload = {
            "action": "START",
            "doimport": True,
            "on_error": "STOP" if exit_on_error else "CONTINUE",
            "operation": task_operation,
            "separator": "COMMA",
            "token": upload_token,
        }

        # Update the operation if the user passes in MERGE or OVERRIDE directly
        if task_operation == "MERGE":
            payload["operation"] = "UPDATE"
            payload["update_method"] = "MERGE"
        elif task_operation == "OVERRIDE":
            payload["operation"] = "UPDATE"
            payload["update_method"] = "OVERRIDE"

        # start the CSV task in job manager
        try:
            res = self.post(
                "fileop",
                params={"_function": "csv_import"},
                json=payload,
                headers=headers,
                cookies=req_cookies,
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        return res.json()

    def __download_complete(self, token: str, filename: str, req_cookies: dict) -> None:
        header = {"Content-type": "application/json"}
        payload = {"token": token}
        try:
            res = self.post(
                "fileop",
                params={"_function": "downloadcomplete"},
                json=payload,
                headers=header,
                cookies=req_cookies,
            )
            logging.info("file %s download complete", filename)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)

    def __download_file(self, download_url, req_cookies):
        header = {"Content-type": "application/force-download"}
        res = None
        try:
            logging.info(download_url)
            res = self.conn.get(
                download_url,
                headers=header,
                stream=True,
                cookies=req_cookies,
                verify=self.ssl_verify,
            )
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
        return res

    def __getgriddata(self, payload: dict, req_cookies) -> dict:
        headers = {"content-type": "application/json"}
        try:
            res = self.post(
                "fileop",
                params={"_function": "getgriddata"},
                json=payload,
                headers=headers,
                cookies=req_cookies,
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        return res.json()

    def __restore_database(
            self, keep_grid_ip: bool, mode: str, upload_token: str, req_cookies: dict
    ) -> dict:
        # set content type back to JSON
        headers = {"content-type": "application/json"}

        # set the request parameters
        payload = {"keep_grid_ip": keep_grid_ip, "mode": mode, "token": upload_token}

        # start the restore
        try:
            res = self.post(
                "fileop",
                params={"_function": "restoredatabase"},
                json=payload,
                headers=headers,
                cookies=req_cookies,
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)
        return res

    def __upload_file(
            self, upload_url: str, upload_file: dict, req_cookies: dict
    ) -> None:
        logging.debug(upload_url)
        try:
            res = self.conn.post(
                upload_url,
                files=upload_file,
                cookies=req_cookies,
                verify=self.ssl_verify,
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

    def __upload_init(self, filename: str) -> dict:
        headers = {"content-type": "application/json"}
        payload = {"filename": filename}
        try:
            res = self.post(
                "fileop",
                params={"_function": "uploadinit"},
                headers=headers,
                json=payload,
            )
            logging.debug(pprint.pformat(res.text))
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise WapiRequestException(err)

        return res.json()

    def __get_cookies(self) -> dict:
        # save the authentication cookie for use in subsequent requests
        ibapauth_cookie = self.conn.cookies["ibapauth"]
        return {"ibapauth": ibapauth_cookie}

    @staticmethod
    def __write_file(filename: str, data: requests.Response) -> None:
        logging.info("writing file: %s", filename)
        with open(filename, "wb") as file:
            for chunk in data.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
