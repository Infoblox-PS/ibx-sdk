# pylint: disable-msg=too-many-locals
"""
Fileop class
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
    download member config file for DNS, DHCP or DHCP6

    :param self: `WAPI` instance
    :param member: Grid Member FQDN value
    :param conf_type: ENUM value for ['DNS', 'DHCP_CONFIG', 'DHCP6_CONFIG]
    :param remote_url: (optional) Remote URL if downloading to alternate location

    :return: string value of the downloaded filename
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
        res = _download_file(self, download_url, req_cookies)
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
        _download_complete(self, download_token, download_file, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    return download_file


def csv_export(
        self,
        wapi_object: str,
        filename: Optional[str] = None) -> None:
    """
    Perform Infoblox CSV Export to file

    :param self: `WAPI` instance
    :param wapi_object: any supported CSV object type to export
    :param filename: (optional) CSV output filename used for output file name.
        If a filename is not provided, the filename is extracted from the URL
        returned by the originating call.

    :return None:
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
        res = _download_file(self, download_url, req_cookies)
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
        _download_complete(self, download_token, filename, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise


def csv_import(
        self,
        task_operation: str,
        csv_import_file: str,
        exit_on_error: bool = False) -> dict:
    """
    run a CSV job in the CSV job manager over WAPI

    Args:
        self: The instance of the class where the method is called
        task_operation: The operation to be performed on the CSV file (e.g. 'import', 'update')
        csv_import_file: The path to the CSV file to be imported
        exit_on_error: Flag indicating whether to exit the program on error (default: False)

    Returns:
        csv_task (dict)

    Raises:
        Exception: If any error occurs during the CSV import process

    """
    (_, filename) = os.path.split(csv_import_file)
    filename = filename.replace('-', '_')

    # Call WAPI fileop Upload INIT
    logging.info('step 1 - request uploadinit %s', filename)
    try:
        obj = _upload_init(self, filename)
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
            _upload_file(self, upload_url, upload_file, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # submit task to CSV Job Manager
        logging.info(
            'step 3 - execute the csv_import %s job on %s',
            task_operation, csv_import_file
        )
        try:
            csvtask = _csv_import(
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


def _upload_init(self, filename: str) -> dict:
    # call uploadinit to get URL and upload_token from server
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


def _upload_file(
        self,
        upload_url: str,
        upload_file: dict,
        req_cookies: dict) -> None:
    """
    upload the file to the file url

    :param self: `WAPI` instance
    :param upload_url: infoblox provided upload file URL
    :param upload_file: upload file name
    :param req_cookies: infoblox authentication cookies

    :return None:
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


def _csv_import(
        self,
        task_operation: str,
        upload_token: str,
        req_cookies: dict,
        exit_on_error: bool = False) -> dict:
    """
    perform CSV import job via WAPI

    Args:
        self: Instance of the class that contains this method.
        task_operation: The type of operation to perform on the tasks.
        upload_token: The token for the CSV file upload.
        req_cookies: The cookies required for the request.
        exit_on_error: Flag indicating whether to exit on error (default is False).

    Returns:
        Dictionary containing the response from the _csv_import operation.

    Raises:
        Exception: If an error occurs during the _csv_import operation.

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
    return csv import task status from CSV Job Manager

    Args:
        self: The instance of the class.
        csvtask: The dictionary containing the CSV import task details.

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
    download csv-errors.#.csv file if any errors are encountered

    :param self: `WAPI` instance
    :param filename: csv import file
    :param job_id: csv job id

    :return None:
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
            res = _download_file(self, download_url, req_cookies)
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
            _download_complete(self, token, filename, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise


def _getgriddata(self, payload: dict, req_cookies) -> dict:
    """
    perform a fileop function call to getgriddata

    :param self: `WAPI` instance
    :param payload: options for fetching grid data
    :param req_cookies: Infoblox authentication cookie

    :return dict: json response
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
    Perform Infoblox Grid Backup to local file

    This method is handy for performing Infoblox Grid Backups to file used often
    to create restore-points. The following calls are performed:

    1. request griddata from the WAPI fileop object
    2. save the griddata to file
    3. signal griddata download to file complete

    :param self: `WAPI` instance
    :param filename: filename or path of the Infoblox backup file to be
        generated (default: database.tgz)

    :return None:
    """
    ibapauth_cookie = self.conn.cookies['ibapauth']
    req_cookies = {'ibapauth': ibapauth_cookie}

    payload = {"type": "BACKUP"}

    logging.info('step 1 - request gridbackup %s', filename)
    try:
        res = _getgriddata(self, payload, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise

    token = res.get('token')
    download_url = res.get('url')

    logging.info("step 2 - saving backup to %s", filename)

    with open(filename, 'wb') as handle:
        try:
            res = _download_file(self, download_url, req_cookies)
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
            _download_complete(self, token, filename, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise


def _download_file(self, download_url, req_cookies):
    """
    Download file from provided download url

    NOTE: this should be used for any of the following:
    * CSV errors file download
    * CSV export file download
    * Grid Backup file download

    :param self: `WAPI` instance
    :param download_url: Infoblox provided download URL
    :param req_cookies: Authentication cookies

    :return: requests response object
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


def _download_complete(
        self,
        token: str,
        filename: str,
        req_cookies: dict) -> None:
    """
    post file downloadcomplete function

    NOTE: this private function should be used whenever a filedownload of any
    kind is complete. Use for the following:

    - CSV errors file download
    - CSV export file
    - Grid backup file downloaded

    :param self: WAPI object
    :param token: download token
    :param filename: filename
    :param req_cookies: auth cookies

    :return None:
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


def _restore_database(
        self,
        keep_grid_ip: bool,
        mode: str,
        upload_token: str,
        req_cookies: dict) -> dict:
    """
    perform fileop function call to restoredatabase

    :param self: is a `WAPI` instance
    :param keep_grid_ip: set this value to `True` to retain the IP address
        configuration settings of the Grid Manager, if `False` the network
        settings will potentially be overwritten with the IP address of the GM
        in the restore file.
    :param mode: restore mode
    :param upload_token: file upload token
    :param req_cookies: infoblox authentication cookie

    :return dict: requests response
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
    method for restore NIOS database file

    This method will perform all the necessary steps in doing a Grid Restore to
    Grid Master. The caller supplies the name of the file to restore, the mode,
    and whether to retain the IP Address settings of the GM or allow it to be
    overwritten.

    This method performs the following calls:

    1. Initiates the file upload by calling _upload_init()
    2. Uploads the file to restore calling _upload_file()
    3. Starts the Grid restore process calling _restore_database()

    :param self: `WAPI` instance
    :param restore_file_name: supply a filename or filepath of an Infoblox Grid
        backup file to restore.
    :param mode: specify a restore mode as any one of `NORMAL`, `FORCED`,
        `CLONE`. Use `NORMAL` when you are restoring a Grid backup file that was
        extracted from the same server you're restoring to. Use `FORCED` to
        restore a Grid backup file to a different Grid Manager. This is most
        often used by PS to restore a customer's Grid onto a different GM in a
        lab environment.
    :param keep_grid_ip: set this value to `True` to retain the Grid Manager's
        network settings and/or IP address. Set it to `False` will cause the
        network settings and IP address to be overwritten w/ the value contained
        in the restore file.

    :return None:
    """
    (_, filename) = os.path.split(restore_file_name)
    filename = os.path.join(_, filename.replace('-', '_'))

    # Call WAPI fileop Upload INIT
    logging.info('step 1 - request uploadinit %s', restore_file_name)
    try:
        obj = _upload_init(self, filename)
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
            _upload_file(self, upload_url, upload_file, req_cookies)
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

        # Execute the restore
        logging.info('step 3 - execute the restore')
        try:
            _restore_database(
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
    # Call WAPI fileop (download) get_support_bundle function
    logging.info(
        'performing get_support_bundle for %s object(s)', member
    )
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
    logging.debug('payload: %s', pprint.pformat(payload))
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
        res = _download_file(self, download_url, req_cookies)
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
        _download_complete(self, download_token, filename, req_cookies)
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
    Fetches log from NIOS and writes it to disk for given type, member, and endpoint

    Args:
        self: The instance of the class calling this method.
        log_type: The type of log files to fetch. This can be one of the LogType enum values.
        endpoint: Optional. The specific endpoint to fetch log files for.
        include_rotated: Optional. Whether to include rotated log files. Default is False.
        member: Optional. The member to fetch log files for.
        msserver: Optional. The specific MSServer to fetch log files for.
        node_type: Optional. The type of node to fetch log files for.

    Raises:
        requests.exceptions.RequestException: If there is an error in making the request or retrieving the log files.

    Returns:
        None

    """
    # Call WAPI fileop (download) get_log_files function
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
        res = _download_file(self, download_url, req_cookies)
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
        _download_complete(self, download_token, filename, req_cookies)
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
