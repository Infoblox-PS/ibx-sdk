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

import json
import logging
import pprint

import requests


def service_restart(self, **kwargs) -> None:
    """
    Restarts specified services of a group, member, or all.

    This method allows for flexible service restarts based on the provided keyword arguments.
    It constructs a data payload from these arguments and sends a POST request to initiate
    the service restart. The method handles request-related exceptions and logs relevant
    information about the operation.

    Args:
        self (WAPI): An instance of the WAPI class
        **kwargs: Arbitrary keyword arguments. These are used to specify which services
                  to restart. If 'services' is not specified, it defaults to restarting 'ALL'.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the POST request.

    Returns:
        None: This method does not return a value but logs the result of the operation,
              indicating the success of the service restart.

    """

    data = {}
    for prop, value in kwargs.items():
        if prop == 'services':
            data[prop] = [value]
        elif value:
            data[prop] = value

    logging.debug(pprint.pformat(data))

    try:
        res = self.post(
            self.grid_ref, params={'_function': 'restartservices'}, json=data
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.info(
            'successfully restarted %s services', data.get('services')
        )


def update_service_status(self, services: str = 'ALL') -> None:
    """Updates the restart status of grid services.

    This method sends a POST request to update the restart status of specified grid services.
    It handles request-related exceptions and logs the response or any errors encountered.

    Args:
        self (WAPI): An instance of the WAPI class
        services (str): The name of the service(s) to check the restart status for.
                        Defaults to 'ALL', indicating all services.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the POST request.

    Returns:
        None: This method does not return a value but logs the response text upon
              successful completion of the request.


    """
    payload = dict(service_option=services)
    try:
        res = self.conn.post(
            f'{self.url}/{self.grid_ref}?_function=requestrestartservicestatus',
            data=json.dumps(payload),
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        logging.info(res.text)


def get_service_restart_status(self) -> dict:
    """Gets the restart status of all member services.

    This method sends a GET request to the specified URL to retrieve the restart status
    of all member services. It handles various exceptions related to the request, such as
    SSL errors, HTTP errors, and other request exceptions, and logs any errors encountered.

    Returns:
        dict: A dictionary containing the restart status of all member services. The
        dictionary is obtained by parsing the JSON response from the request.

    Raises:
        requests.exceptions.SSLError: If an SSL error occurs during the request.
        requests.exceptions.HTTPError: If an HTTP error occurs during the request.
        requests.exceptions.RequestException: For other request-related errors.

    """

    try:
        res = self.conn.get(
            f'{self.url}/restartservicestatus',
            verify=self.ssl_verify
        )
        res.raise_for_status()
    except requests.exceptions.SSLError as err:
        logging.error(err)
        raise
    except requests.exceptions.HTTPError as err:
        logging.error(err)
        raise
    except requests.exceptions.RequestException as err:
        logging.error(err)
        raise
    else:
        return res.json()
