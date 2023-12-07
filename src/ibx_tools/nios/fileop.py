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

import datetime
import json
import logging
import os
import pprint
from typing import Optional

import requests.exceptions

from ibx_tools.util import util


def member_config(
        self,
        member: str,
        conf_type: str,
        remote_url: str = None) -> str:
    """
    Downloads a member config file for DNS, DHCP, or DHCP6.

    Args:
        self (WAPI): An instance of WAPI class.
        member (str): Fully Qualified Domain Name value for the grid member.
        conf_type (str): Specifies the type of configuration. It can be one of the following -
                         'DNS', 'DHCP_CONFIG', 'DHCP6_CONFIG'.
        remote_url (str, optional): If an alternate location for downloading is specified,
                                    this stores the URL of that location.

    Returns:
        str: The filename of the downloaded config file.

    The function first logs the initiation of downloading process and prepares a payload
    with member and type details. If a remote url was specified, it's added to the payload.
    It then attempts a post request to download the config file for the specified member.
    If the post request encounters an exception, it's logged and re-raised.

    Upon receiving the response, it extracts the download url and the download token from it.
    It retrieves the `ibapauth` cookie from the cookie jar and logs the download url.

    It then attempts to download the file from the obtained url. If the download encounters
    an exception, it's logged and re-raised otherwise it proceeds to write the downloaded
    data into the file.

    The function finally notifies the grid that file download is complete by calling
    `__download_complete` function. If it encounters an exception, it's logged and re-raised.
    """

    conf_type = conf_type.upper()
    logging.info(
        'fetching %s config file for grid member %s',
        conf_type, member
    )
    payload = {'member': member, 'type': conf_type}
    if remote_url:
        payload['remote_url'] = remote_url
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=getmemberdata',
            data=json.dumps(payload),
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    obj = res.json()
    download_url = obj.get('url')
    download_token = obj.get('token')

    # get auth cookie from cookie jar
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    logging.info('downloading data from %s', download_url)
    try:
        res = __download_file(self, download_url, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    download_file = util.get_csv_from_url(download_url)

    logging.info('writing data to %s file', download_file)
    with open(download_file, 'wb') as handle:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                handle.write(chunk)

    # notify grid file downloadcomplete
    try:
        __download_complete(self, download_token, download_file, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    return download_file


def csv_export(
        self,
        wapi_object: str,
        filename: Optional[str] = None) -> None:
    """
    Performs Infoblox CSV Export to a file.

    Args:
        self (WAPI): An instance of WAPI class.
        wapi_object (str): Any supported CSV object type to export.
        filename (str, optional): The name of the output CSV file. If a filename
                                  is not provided, the name is extracted from the URL
                                  returned by the originating call.

    This function initiates a CSV export for a specified WAPI object. Logging is done at
    the commencement of the operation.

    A payload is prepared containing the mentioned WAPI object and a POST request is
    triggered. In case of exception during this request, it is logged and then re-raised.

    Upon successful request, the response is processed for a download URL and token. An
    `ibapauth` cookie is then retrieved from the cookie jar, which is logged, and the
    function attempts to download the file from the obtained URL. If an exception occurs
    during the download, it's logged and re-raised.

    If no filename was provided, one is obtained from the download URL. The function
    then writes the downloaded data into the file.

    Finally, it notifies the grid about the completion of the download via the
    `__download_complete` function and returns None. If the notification process
    encounters an exception, it's logged and re-raised.
    """

    if filename:
        (_, filename) = os.path.split(filename)
        filename = os.path.join(_, filename.replace('-', '_'))

    # Call WAPI fileop  csv_export function
    logging.info(
        'performing csv export for %s object(s)', wapi_object
    )
    payload = {'_object': wapi_object}
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=csv_export',
            data=json.dumps(payload),
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    obj = res.json()
    download_url = obj.get('url')
    download_token = obj.get('token')

    # get auth cookie from cookie jar
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    logging.info('downloading data from %s', download_url)
    try:
        res = __download_file(self, download_url, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    if not filename:
        filename = util.get_csv_from_url(download_url)

    logging.info('writing data to %s file', filename)
    with open(filename, 'wb') as handle:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                handle.write(chunk)

    # notify grid file downloadcomplete
    try:
        __download_complete(self, download_token, filename, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise


def csv_import(
        self,
        task_operation: str,
        csv_import_file: str,
        exit_on_error: bool = False) -> dict:
    """
    Initiates a CSV import job via WAPI.

    This method facilitates the execution of a CSV import job using the Infoblox WAPI. It requires
    specifying the type of task operation to be performed on the CSV file, such as import or update.
    The method also allows control over the behavior when encountering errors during the import process.

    Args:
        self: The instance of the class where the method is called.
        task_operation (str): The operation to be performed on the CSV file (e.g., 'IMPORT', 'UPDATE').
        csv_import_file (str): The path to the CSV file to be imported.
        exit_on_error (bool, optional): If True, the import will halt on encountering an error;
                                        if False, it continues. Defaults to False.

    Returns:
        dict: A dictionary representing the status of the CSV import job initiation. This typically
              includes details like job reference and initial status.

    Raises:
        Exception: If an error occurs during the CSV import process.

    Example:

    ```python
            wapi_instance = WAPI(...)
            csv_task = wapi_instance.csv_import(
                task_operation='IMPORT',
                csv_import_file='/path/to/file.csv',
                exit_on_error=False
            )
            print(csv_task)
    ```
    """
    (_, filename) = os.path.split(csv_import_file)
    filename = filename.replace('-', '_')

    # Call WAPI fileop Upload INIT
    logging.info('step 1 - request uploadinit %s', filename)
    try:
        obj = __upload_init(self, filename)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    upload_url = obj.get('url')
    token = obj.get('token')

    # save the authentication cookie for use in subsequent requests
    ibapauth_cookie = self.conn.cookies['ibapauth']

    # specify a file handle for the file data to be uploaded
    with open(csv_import_file, 'rb') as csvfile:
        # reset to top of the file
        csvfile.seek(0)
        upload_file = {'file': csvfile.read()}

        # use the ibapauth cookie for auth to the upload_url
        req_cookies = {'ibapauth': ibapauth_cookie}

        # Upload the contents of the CSV file
        logging.info(
            'step 2 - post the files using the upload_url provided'
        )
        try:
            __upload_file(self, upload_url, upload_file, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # submit task to CSV Job Manager
        logging.info(
            'step 3 - execute the csv_import %s job on %s',
            task_operation, csv_import_file
        )
        try:
            csvtask = __csv_import(
                self,
                task_operation.upper(),
                token,
                req_cookies,
                exit_on_error
            )
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise
        else:
            return csvtask


def __upload_init(self, filename: str) -> dict:
    """
    Initializes a file upload process in the Infoblox WAPI.

    This private method is used to initiate a file upload operation. It sends a POST request to the WAPI
    with the filename to be uploaded. In response, the server provides a URL and an upload token, which are
    necessary for the subsequent file upload process.

    Args:
        self: Instance of the `WAPI` class.
        filename (str): The name of the file to be uploaded.

    Returns:
        dict: A dictionary containing the response from the WAPI. This includes the URL for the file upload
              and an upload token.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the initialization of the file upload.

    """

    headers = {'content-type': 'application/json'}
    payload = {'filename': filename}
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=uploadinit',
            data=json.dumps(payload),
            headers=headers,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    logging.debug(pprint.pformat(res.text))
    return res.json()


def __upload_file(
        self,
        upload_url: str,
        upload_file: dict,
        req_cookies: dict) -> None:
    """
    Uploads a file to a specified URL using the Infoblox WAPI.

    This private method handles the uploading of a file to a provided Infoblox WAPI URL. It uses
    HTTP POST method for uploading and requires authentication cookies. The method is designed to
    work within the WAPI class for internal operations related to file uploading.

    Args:
        self: Instance of the `WAPI` class.
        upload_url (str): Infoblox provided URL to which the file needs to be uploaded.
        upload_file (dict): Dictionary representing the file to upload. The format is typically
                            {'file': ('filename', fileobj)}.
        req_cookies (dict): Dictionary containing the authentication cookies required for Infoblox.

    Returns:
        None: The method returns nothing. It logs the response text for debugging purposes.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the file upload process.

    """
    # Perform the actual upload
    try:
        res = self.conn.post(
            upload_url,
            files=upload_file,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    logging.debug(pprint.pformat(res.text))


def __csv_import(
        self,
        task_operation: str,
        upload_token: str,
        req_cookies: dict,
        exit_on_error: bool = False) -> dict:
    """
    Performs a CSV import job via WAPI.

    This private method initiates a CSV import task in the Infoblox WAPI. It sends a POST request
    with specified parameters to import data from a CSV file into the WAPI. The method allows
    specifying the type of operation (e.g., insert, update, merge), handling of errors during import,
    and requires an upload token and cookies for authentication.

    Args:
        self: Instance of the class containing this method.
        task_operation (str): The type of operation to perform (e.g., 'INSERT', 'UPDATE').
        upload_token (str): Token received after successfully uploading the CSV file.
        req_cookies (dict): Cookies required for making the WAPI request.
        exit_on_error (bool, optional): If True, the import will stop on encountering an error;
                                        continues otherwise. Default is False.

    Returns:
        dict: A dictionary containing the response from the CSV import operation. This includes
              details about the import task initiation, such as status and task reference.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the CSV import operation.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> response = wapi_instance.__csv_import(
                task_operation='INSERT',
                upload_token='some-token',
                req_cookies={'session_id': '123'},
                exit_on_error=False
            )
        >>> print(response)
    """
    headers = {'content-type': 'application/json'}

    # set the request parameters
    payload = {
        'action': "START",
        'doimport': True,
        'on_error': 'STOP' if exit_on_error else 'CONTINUE',
        'operation': task_operation,
        'separator': 'COMMA',
        'token': upload_token
    }

    # Update the operation if the user passes in MERGE or OVERRIDE directly
    if task_operation == 'MERGE':
        payload['operation'] = 'UPDATE'
        payload['update_method'] = 'MERGE'
    elif task_operation == 'OVERRIDE':
        payload['operation'] = 'UPDATE'
        payload['update_method'] = 'OVERRIDE'

    # start the CSV task in job manager
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=csv_import',
            data=json.dumps(payload),
            headers=headers,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.debug(pprint.pformat(res.text))

    return res.json()


def csvtask_status(self, csvtask: dict) -> dict:
    """
    Fetches the status of a CSV import task from the CSV Job Manager.

    This method queries the status of a specific CSV import task identified by the task reference
    in the provided csvtask dictionary. It makes an HTTP GET request to the WAPI endpoint and
    returns the current status of the task in a JSON format.

    Args:
        self: The instance of the WAPI class.
        csvtask (dict): A dictionary containing details of the CSV import task. It should include
                        the '_ref' key to uniquely identify the task.

    Returns:
        dict: A dictionary containing the JSON response with the status of the CSV import task.
              This includes details such as current state, progress, and any errors.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request to the WAPI endpoint.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> task_details = {'csv_import_task': {'_ref': 'task:abc123'}}
        >>> status = wapi_instance.csvtask_status(task_details)
        >>> print(status)
    """
    _ref = csvtask['csv_import_task']['_ref']
    logging.debug('Checking status of csvimporttask %s', _ref)
    try:
        res = self.conn.get(f'{self.url}/{_ref}', verify=self.ssl_verify)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.debug(res.json())

    return res.json()


def get_csv_errors_file(self, filename: str, job_id: str) -> None:
    """
    Downloads the CSV errors file for a specified job.

    This method retrieves the errors file generated from a CSV import job in Infoblox WAPI, if any errors
    were encountered. It first requests the error log file's download URL and token, and then proceeds to
    download the file. The file is saved with the provided filename.

    Args:
        self: Instance of the `WAPI` class.
        filename (str): Name of the CSV file that was imported, used for naming the errors file.
        job_id (str): Unique identifier of the CSV import job.

    Returns:
        None: This method does not return a value. It writes the errors file to the local file system.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the file download process or
                                              in any of the intermediate steps.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> wapi_instance.get_csv_errors_file('imported_data.csv', '1234567890')
    """

    logging.debug('fetching csv-errors file for job id %s', job_id)
    payload = {'import_id': job_id}
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=csv_error_log',
            data=json.dumps(payload),
            verify=self.ssl_verify
        )
        res.raise_for_status()
        logging.debug(pprint.pformat(res.text))
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    obj = res.json()
    token = obj.get('token')
    download_url = obj.get('url')

    # save the authentication cookie for use in subsequent requests
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    filename = f'csv-errors-{filename}.csv'
    with open(filename, 'wb') as handle:
        try:
            res = __download_file(self, download_url, req_cookies)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # iterate over the result content and write it out to file
        for block in res.iter_content(chunk_size=1024):
            if block:
                handle.write(block)

        # We're done - so post to downloadcomplete function
        try:
            __download_complete(self, token, filename, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise


def __getgriddata(self, payload: dict, req_cookies) -> dict:
    """
    Executes a 'getgriddata' file operation call to the Infoblox WAPI.

    This private method is designed for internal use within the WAPI class to perform 'getgriddata'
    operations. It sends a POST request with the specified payload to the WAPI, retrieving grid data
    based on the options provided in the payload. The method requires Infoblox authentication cookies.

    Args:
        self: Instance of the `WAPI` class.
        payload (dict): A dictionary containing options and parameters for fetching grid data.
        req_cookies: Infoblox authentication cookies required for making the request.

    Returns:
        dict: A dictionary containing the JSON response from the WAPI. This includes the requested grid data.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request to the WAPI endpoint.

    """

    # set content type back to JSON
    headers = {'content-type': 'application/json'}
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=getgriddata',
            data=json.dumps(payload),
            headers=headers,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.debug(pprint.pformat(res.text))

    return res.json()


def grid_backup(self, filename: str = 'database.tgz') -> None:
    """
    Performs a backup of the Infoblox Grid and saves it to a local file.

    This method facilitates creating a backup of the Infoblox Grid. It involves several steps,
    including requesting grid data from the WAPI file operation object, saving the grid data to a file,
    and signaling the completion of the download. The backup file is saved with the specified filename.

    Args:
        self: Instance of the `WAPI` class.
        filename (str, optional): The name or path of the file where the Infoblox backup will be saved.
                                  Defaults to 'database.tgz'.

    Returns:
        None: The method does not return a value. It performs the backup operation and saves the file locally.

    Raises:
        requests.exceptions.RequestException: If an error occurs during any step of the backup process.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> wapi_instance.grid_backup('backup_file.tgz')
    """

    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    payload = {"type": "BACKUP"}

    logging.info('step 1 - request gridbackup %s', filename)
    try:
        res = __getgriddata(self, payload, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    token = res.get('token')
    download_url = res.get('url')

    logging.info("step 2 - saving backup to %s", filename)

    with open(filename, 'wb') as handle:
        try:
            res = __download_file(self, download_url, req_cookies)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # iterate over the result content and write it out to file
        for block in res.iter_content(chunk_size=1024):
            if block:
                handle.write(block)

        # we're done - post downloadcomplete function using the token
        try:
            __download_complete(self, token, filename, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise


def __download_file(self, download_url, req_cookies):
    """
    Downloads a file from a specified Infoblox URL.

    This private method is part of the `WAPI` class and is used for downloading files from the Infoblox WAPI.
    It is commonly used for downloading CSV errors files, CSV export files, and Grid backup files. The method
    sends a GET request to the provided URL and returns the response object, which contains the downloaded file
    data. It requires authentication cookies for access.

    Args:
        self: Instance of the `WAPI` class.
        download_url (str): URL provided by Infoblox for downloading the file.
        req_cookies (dict): Dictionary containing the authentication cookies required for the request.

    Returns:
        requests.Response: The response object from the GET request, containing the file data.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the file download process.

    """

    header = {'Content-type': 'application/force-download'}
    try:
        res = self.conn.get(
            download_url,
            headers=header,
            stream=True,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    return res


def __download_complete(
        self,
        token: str,
        filename: str,
        req_cookies: dict) -> None:
    """
    Notifies the completion of a file download process in the Infoblox WAPI.

    This private method is used to signal the completion of a file download from the Infoblox WAPI.
    It is a follow-up step typically performed after downloading files such as CSV error logs, CSV export files,
    or Grid backup files. The method sends a POST request with a download token to the WAPI.

    Args:
        self: Instance of the `WAPI` class.
        token (str): The download token associated with the file download.
        filename (str): The name of the file that was downloaded.
        req_cookies (dict): Dictionary containing the authentication cookies required for the request.

    Returns:
        None: This method does not return a value. It performs a notification operation.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the notification process.

    """
    header = {'Content-type': 'application/json'}
    payload = {'token': token}
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=downloadcomplete',
            data=(json.dumps(payload)),
            headers=header,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        logging.info("file %s download complete", filename)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise


def __restore_database(
        self,
        keep_grid_ip: bool,
        mode: str,
        upload_token: str,
        req_cookies: dict) -> dict:
    """
    Performs a database restore operation in the Infoblox WAPI.

    This private method is responsible for initiating a database restore operation via the Infoblox WAPI.
    It posts a request with specific parameters to control the restore process, including whether to retain
    the Grid Manager's IP address, the mode of restoration, and a token for the uploaded file.

    Args:
        self: Instance of the `WAPI` class.
        keep_grid_ip (bool): If True, retains the Grid Manager's IP address configuration settings.
                             If False, network settings may be overwritten with the IP address in the
                             restore file.
        mode (str): The mode of restoration (e.g., 'NORMAL', 'FORCED').
        upload_token (str): Token received after successfully uploading the restore file.
        req_cookies (dict): Dictionary containing the authentication cookies required for the request.

    Returns:
        dict: A dictionary containing the JSON response from the WAPI. This includes details about
              the restore operation initiation.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the restore operation.

    """
    # set content type back to JSON
    headers = {'content-type': 'application/json'}

    # set the request parameters
    payload = {
        "keep_grid_ip": keep_grid_ip,
        "mode": mode,
        "token": upload_token
    }

    # start the restore
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=restoredatabase',
            data=json.dumps(payload),
            headers=headers,
            cookies=req_cookies,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.debug(pprint.pformat(res.text))
    return res


def grid_restore(self,
                 restore_file_name: str,
                 mode: str,
                 keep_grid_ip: bool) -> None:
    """
    Restores the Infoblox NIOS database from a backup file.

    This method executes a series of steps to restore the Infoblox Grid database from a specified backup file.
    It allows the user to specify the restore mode and whether to keep the current Grid Manager's IP settings.
    The method involves initializing the file upload, uploading the backup file, and then initiating the grid
    restore process.

    Args:
        self: Instance of the `WAPI` class.
        restore_file_name (str): The name or path of the Infoblox grid backup file to be restored.
        mode (str): The restore mode. Can be one of 'NORMAL', 'FORCED', or 'CLONE'.
        keep_grid_ip (bool): If True, retains the Grid Manager's network settings and IP address.
                             If False, these settings will be overwritten with the values in the restore file.

    Returns:
        None: This method does not return a value. It performs the restore operation.

    Raises:
        requests.exceptions.RequestException: If an error occurs during any step of the restore process.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> wapi_instance.grid_restore('backup_file.tgz', 'NORMAL', True)
    """
    (_, filename) = os.path.split(restore_file_name)
    filename = os.path.join(_, filename.replace('-', '_'))

    # Call WAPI fileop Upload INIT
    logging.info('step 1 - request uploadinit %s', restore_file_name)
    try:
        obj = __upload_init(self, filename)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    upload_url = obj.get('url')
    token = obj.get('token')

    # save the authentication cookie for use in subsequent requests
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    # specify a file handle for the file data to be uploaded
    with open(restore_file_name, "rb") as restore_file:
        # Upload the contents of the CSV file
        logging.info('step 2 - post the files using the upload_url provided')
        upload_file = {'filedata': restore_file}
        try:
            __upload_file(self, upload_url, upload_file, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # Execute the restore
        logging.info('step 3 - execute the restore')
        try:
            __restore_database(
                self,
                keep_grid_ip,
                mode,
                token,
                req_cookies
            )
        except requests.exceptions.RequestException as err:
            logging.error('step 3 - Error: %s', err)
            raise
        logging.info("Grid restore successful!")


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
    Fetches and downloads a support bundle from the specified Infoblox member.

    This method requests a support bundle from an Infoblox member and downloads it. The support bundle may
    include various data like cached zone data, core files, log files, and more, depending on the options
    specified. The method sends a request to the WAPI and handles the download and saving of the resulting
    support bundle file.

    Args:
        self: Instance of the `WAPI` class.
        member (str): The name or IP address of the target member.
        cached_zone_data (bool, optional): If True, includes cached zone data in the bundle. Defaults to False.
        core_files (bool, optional): If True, includes core files in the bundle. Defaults to False.
        log_files (bool, optional): If True, includes log files in the bundle. Defaults to False.
        nm_snmp_logs (bool, optional): If True, includes NIOS Maintenance SNMP logs in the bundle. Defaults to False.
        recursive_cache_file (bool, optional): If True, includes the cache file recursively. Defaults to False.
        remote_url (str, optional): URL of a remote server to upload the support bundle to. Defaults to None.
        rotate_log_files (bool, optional): If True, rotates log files after creating the support bundle. Defaults to False.

    Returns:
        None: This method does not return a value. It performs the operation of fetching and saving the support bundle.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the request or file download process.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> wapi_instance.get_support_bundle(
                member='member1',
                cached_zone_data=True,
                core_files=True,
                log_files=True
            )
    """

    logging.info('performing get_support_bundle for %s object(s)', member)
    payload = {
        "member": member,
        "cached_zone_data": cached_zone_data,
        "core_files": core_files,
        "log_files": log_files,
        "nm_snmp_logs": nm_snmp_logs,
        "recursive_cache_file": recursive_cache_file,
        "rotate_log_files": rotate_log_files
    }
    if remote_url:
        payload["remote_url"] = remote_url
    json_payload = json.dumps(payload)
    logging.debug('payload: %s', pprint.pformat(json_payload))
    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=get_support_bundle',
            data=json_payload,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    obj = res.json()
    download_url = obj.get('url')
    download_token = obj.get('token')

    # get auth cookie from cookie jar
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    logging.info('downloading data from %s', download_url)
    try:
        res = __download_file(self, download_url, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    date_time = str(datetime.datetime.now().strftime('%Y%m%d%S'))
    filename = f'{date_time}-{member}-SupportBundle.tgz'

    logging.info('writing data to %s file', filename)
    with open(filename, 'wb') as handle:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                handle.write(chunk)

    # notify grid file downloadcomplete
    try:
        __download_complete(self, download_token, filename, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise


def get_log_files(
        self,
        log_type: str,
        endpoint: Optional[str] = None,
        include_rotated: bool = False,
        member: Optional[str] = None,
        msserver: Optional[str] = None,
        node_type: Optional[str] = None
):
    """
    Fetches specified log files from NIOS and writes them to disk.

    This method is used to retrieve log files of a specified type from the NIOS system. It can target
    specific members, endpoints, or MSServers, and optionally include rotated log files. The logs are
    downloaded and saved to a file on disk.

    Args:
        self: Instance of the `WAPI` class calling this method.
        log_type (str): The type of log files to fetch, as defined in the LogType enum.
        endpoint (str, optional): Specific endpoint to fetch log files for. Default is None.
        include_rotated (bool, optional): Whether to include rotated log files. Default is False.
        member (str, optional): Specific member to fetch log files for. Default is None.
        msserver (str, optional): Specific MSServer to fetch log files for. Default is None.
        node_type (str, optional): Type of node to fetch log files for. Default is None.

    Returns:
        None: This method does not return a value. It performs the operation of fetching and saving the log files.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the request or file download process.

    Example:
        >>> wapi_instance = WAPI(...)
        >>> wapi_instance.get_log_files(
                log_type='syslog',
                member='member1',
                include_rotated=True
            )
    """

    logging.info('fetching %s log files for %s', log_type, member)
    payload = {
        "log_type": log_type,
        "include_rotated": include_rotated
    }

    if endpoint:
        payload["endpoint"] = endpoint
    if member:
        payload["member"] = member
    if node_type:
        payload["node_type"] = node_type
    if msserver:
        payload["msserver"] = msserver
    json_payload = json.dumps(payload)

    logging.debug("json payload %s", json_payload)

    try:
        res = self.conn.post(
            f'{self.url}/fileop?_function=get_log_files',
            data=json_payload,
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    obj = res.json()
    download_url = obj.get('url')
    download_token = obj.get('token')

    # get auth cookie from cookie jar
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    logging.info('downloading data from %s', download_url)
    try:
        res = __download_file(self, download_url, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    date_time = str(datetime.datetime.now().strftime('%Y%m%d%S'))
    filename = f'{date_time}-{member}-{log_type}.tgz'

    logging.info('writing data to %s file', filename)
    with open(filename, 'wb') as handle:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                handle.write(chunk)

    # notify grid file downloadcomplete
    try:
        __download_complete(self, download_token, filename, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
