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
import ssl
from typing import Union, Any, Optional, List

import httpx
import urllib3

from ibx_sdk.nios.exceptions import (
    WapiInvalidParameterException,
    WapiRequestException,
)
from ibx_sdk.nios.fileop import NiosFileopMixin
from ibx_sdk.nios.service import NiosServiceMixin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Gift(httpx.Client, NiosServiceMixin, NiosFileopMixin):
    """Handles interactions with the Infoblox WAPI.

    This class provides a range of classes to interact with Infoblox WAPI,
    including session management, data retrieval, file operations, and service management.

    Attributes:
        grid_mgr (str): IP address or hostname of the Grid Manager.
        wapi_ver (str): Version of the Infoblox WAPI.
        ssl_verify (bool): Flag to determine SSL certificate verification.
        conn (httpx.Client, optional): Active session to the WAPI grid. Default is None.
        grid_ref (str, optional): Reference ID of the connected grid. Default is None.

    Examples:

    Initialize the WAPI instance with a dictionary of properties:

    ```py

    wapi_properties = {
        'grid_mgr': 'gm.example.com',
        'wapi_ver': '2.11',
        'ssl_verify': False
    }
    wapi = Gift(wapi_properties)

    wapi.connect(username='admin', password='infoblox')

    ```

    Build up the WAPI instance one property at a time:

    ```python

    wapi = Gift()

    wapi.grid_mgr = 'gm.example.com'
    wapi.wapi_ver = '2.11'
    wapi.ssl_verify = False

    wapi.connect(username='admin', password='infoblox')

    ```
    """

    def __init__(
        self,
        grid_mgr: str = None,
        wapi_ver: str = "2.5",
        ssl_verify: bool | str = False,
        timeout: httpx.Timeout = 10.0,
    ) -> None:
        super().__init__()
        self.grid_mgr = grid_mgr
        self.wapi_ver = wapi_ver
        self.ssl_verify = ssl_verify
        self.timeout = timeout
        self.conn = None
        self.grid_ref = None

    def __repr__(self):
        args = []
        for key, value in self.__dict__.items():
            args.append(f"{key}={value}")
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

        wapi = Gift()
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
            return f"https://{self.grid_mgr}/wapi/v{self.wapi_ver}"
        return ""

    def connect(
        self,
        username: str = None,
        password: str = None,
        certificate: str = None,
    ) -> None:
        """
        Make a connection to the grid manager using the WAPI instance

        Args:
            username: A string representing the username for the connection. (default: None)
            password: A string representing the password for the connection. (default: None)
            certificate: A string representing the certificate for the connection. (default: None)
        Raises:
            WapiInvalidParameterException: If neither a username and password nor a certificate
                                           is provided.

        """
        if not self.url:
            logging.error("invalid url %s - unable to connect!", self.url)
            raise WapiInvalidParameterException

        if username and password:
            self.__basic_auth_request(username, password)
        elif certificate:
            self.__certificate_auth_request(certificate)
        else:
            raise WapiInvalidParameterException

    def __certificate_auth_request(self, certificate: str) -> dict | None:
        """
        This private method performs a certificate authentication request to the API. It uses the
        provided certificate to establish a connection with the API server using the httpx
        library.

        Args:
            certificate (str): The certificate to be used for authentication with the API.

        Returns:
            grid _ref (dict): A dictionary

        Raises:
            WapiRequestException: If there is an error with the request to the API.

        """
        ctx = ssl.create_default_context()
        ctx.load_cert_chain(certfile=certificate)
        if self.ssl_verify:
            ctx.load_verify_locations(cafile=self.ssl_verify)
        else:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        try:
            conn = httpx.Client(verify=ctx, timeout=self.timeout)
            res = conn.get(f"{self.url}/grid")
            res.raise_for_status()
            try:
                grid = res.json()
                self.conn = conn
                self.grid_ref = grid[0].get("_ref", "")
                return self.grid_ref
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {res.text}")
                raise WapiRequestException(res.text) from exc
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc

    def __basic_auth_request(self, username: str, password: str) -> dict | None:
        """
        This private method makes a request to the specified URL with basic authentication using
        the provided username and password. It stores the session connection in the instance
        attribute 'conn*' and the grid reference in the instance attribute 'grid_ref'.

        Note:
            This method requires the 'httpx' library to be installed.

        Args:
            username (str): The username for basic authentication.
            password (str): The password for basic authentication.

        Returns:
            grid _ref (dict): A dictionary

        Raises:
            WapiRequestException: If an error occurs during the request.
        """
        auth = httpx.BasicAuth(username, password)

        ctx = ssl.create_default_context()
        if self.ssl_verify:
            ctx.load_verify_locations(cafile=self.ssl_verify)
        else:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        try:
            conn = httpx.Client(auth=auth, verify=ctx, timeout=self.timeout)
            res = conn.get(f"{self.url}/grid")
            res.raise_for_status()
            try:
                grid = res.json()
                self.conn = conn
                self.grid_ref = grid[0].get("_ref", "")
                return self.grid_ref
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {exc}")
                raise WapiRequestException(res.text) from exc
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc

    def object_fields(self, wapi_object: str) -> Union[str, None]:
        """
        Retrieves the object fields for a specified WAPI object.

        Args:
            wapi_object (str): The name of the WAPI object for which to retrieve the fields.

        Returns:
            Union[str, None]: A string containing the fields separated by commas, or None if an
            error occurred.

        Raises:
            WapiRequestException: If there was an error connecting to the WAPI service.

        Example:

        ```py
        wapi = Gift()
        fields = wapi.object_fields('record:host')
        if fields is not None:
            print(f"Fields: {fields}")
        ```
        """
        try:
            logging.debug("trying %s/%s?_schema", self.url, wapi_object)
            res = self.conn.get(f"{self.url}/{wapi_object}?_schema")
            res.raise_for_status()
            try:
                data = res.json()
                fields = ",".join(
                    field["name"]
                    for field in data.get("fields")
                    if "r" in field.get("supports")
                )
                return fields
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {exc}")
                raise WapiRequestException(res.text) from exc
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc

    def max_wapi_ver(self) -> None:
        """
        Retrieves and sets the maximum supported version of the WAPI.

        This method queries the WAPI to find the highest supported version and updates
        the `wapi_ver` attribute of the instance with this value. It does not return
        any value.

        Raises:
            WapiRequestException: If there is an error in making the GET request to retrieve
                                  the WAPI version. This could be due to network issues,
                                  authentication errors,
                                  or other problems in the request process.

        Example Usage:
        ```python
        session = Gift()
        session.max_wapi_ver()
        print(session.wapi_ver)  # Prints the maximum supported WAPI version
        ```

        Note:
            This method updates the `wapi_ver` attribute of the WAPI session instance.
        """

        url = f"https://{self.grid_mgr}/wapi/v1.0/?_schema"
        try:
            logging.debug("trying %s", url)
            res = self.conn.get(url)
            res.raise_for_status()
            try:
                data = res.json()
                versions = data.get("supported_versions")
                versions.sort(key=lambda s: list(map(int, s.split("."))))
                logging.debug(versions)
                max_wapi_ver = versions.pop()
                self.wapi_ver = max_wapi_ver
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {exc}")
                raise WapiRequestException(res.text) from ValueError
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc

    def get(
        self, wapi_object: str, params: Optional[dict] = None, **kwargs: Any
    ) -> httpx.Response:
        """
        Return WAPI object(s).
        Args:
            wapi_object (str): The name of the WAPI object to retrieve.
            params (Optional[dict]): Optional parameters to include in the request URL.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            Response: The response object containing the result of the request.
        """
        url = f"{self.url}/{wapi_object}"
        res = None
        try:
            res = self.conn.get(url, params=params, **kwargs)
            res.raise_for_status()
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(res.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(res.text) from exc
        return res

    def getone(
        self, wapi_object: str, params: Optional[dict] = None, **kwargs: Any
    ) -> str:
        """
        Return the reference of a single WAPI object.

        Args:
            wapi_object: A string representing the object to retrieve data from.
            params: Optional dictionary of parameters to include in the request.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            str: A string response containing the _ref of the WAPI object.

        Raises:
            WapiRequestException: If multiple data records were returned or no data was returned.
        """
        url = f"{self.url}/{wapi_object}"
        response = None
        try:
            response = self.conn.request("get", url, params=params, **kwargs)
            response.raise_for_status()
            try:
                data = response.json()
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {response.text}")
                raise WapiRequestException(response.text) from exc
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(response.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(response.text) from exc
        else:
            if len(data) > 1:
                raise WapiRequestException(
                    "Multiple data records were returned"
                )
            elif len(data) == 0:
                raise WapiRequestException("No data was returned")
        return data[0].get("_ref", "")

    def post(
        self,
        wapi_object: str,
        data: Optional[Union[dict, str]] = None,
        json: Optional[dict] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Create a POST request to create a WAPI object.

        Args:
            wapi_object: The object to which the POST request is being made.
            data (optional): The data to be sent in the body of the request.
                             Can be a dictionary or a string. Default is None.
            json (optional): The JSON data to be sent in the body of the request.
                             Should be a dictionary. Default is None.
            **kwargs (optional): Additional keyword arguments to be passed to the request.

        Returns:
            Response: The response object containing the server's response to the POST request.
        """
        url = f"{self.url}/{wapi_object}"
        res = None
        try:
            res = self.conn.request("post", url, data=data, json=json, **kwargs)
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(res.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(res.text) from exc
        return res

    def put(
        self,
        wapi_object_ref: str,
        data: Optional[Union[dict, str]] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Create a PUT request to update a WAPI object by its _ref.

        Args:
            wapi_object_ref: The reference string for the WAPI object.
            data: Optional data to be sent with the request. Can be a dictionary or a string. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the request.

        Returns:
            Response: The response object for the PUT request.
        """
        url = f"{self.url}/{wapi_object_ref}"
        res = None
        try:
            res = self.conn.request("put", url, data=data, **kwargs)
            return res
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(res.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(res.text) from exc

    def delete(self, wapi_object_ref: str, **kwargs: Any) -> httpx.Response:
        """
        Args:
            wapi_object_ref (str): A string representing the reference to the WAPI object that
                                   needs to be deleted.
            **kwargs (Any): Additional keyword arguments that can be passed to the `request` method
                            of the connection object.

        Returns:
            A `Response` object representing the response received from the server.

        """
        url = f"{self.url}/{wapi_object_ref}"
        res = None
        try:
            res = self.conn.request("delete", url, **kwargs)
            return res
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(res.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(res.text) from exc

    def get_paginated(
        self,
        wapi_object: str,
        limit: int = 1000,
        params: Optional[dict] = None,
        **kwargs: Any
    ) -> List[dict]:
        """
        Fetches paginated data from the WAPI API.

        This method retrieves data in chunks using a pagination mechanism. The function
        handles API responses, manages pagination parameters, and consolidates the
        results into a list. It raises exceptions if timeout, HTTP status errors, or
        request errors are encountered during the process.

        Args:
            wapi_object: The name of the WAPI object to fetch data from.
            limit: Maximum number of records to retrieve per API request. Defaults to 1000.
            params: Additional query parameters to include in the request. Defaults to None.
            **kwargs: Additional keyword arguments passed to the HTTP GET request.

        Returns:
            A list of dictionaries containing the retrieved data from the WAPI API.

        Raises:
            WapiRequestException: If there is a timeout, HTTP status error, or
            request-related error during the API call.
        """
        results = []
        params = params.copy() if params else {}

        params.update({
            "_paging": 1,
            "_return_as_object": 1,
            "_max_results": limit,
        })

        url = f"{self.url}/{wapi_object}"
        response = None

        try:
            while True:
                response = self.conn.get(url, params=params, **kwargs)
                response.raise_for_status()

                data = response.json()
                results.extend(data.get("result", []))

                next_page_id = data.get("next_page_id")
                if not next_page_id:
                    break

                params["_page_id"] = next_page_id

        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error while fetching {url}: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP status error while fetching {url}: {exc}")
            raise WapiRequestException(response.text) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error while fetching {url}: {exc}")
            raise WapiRequestException(str(exc)) from exc

        return results