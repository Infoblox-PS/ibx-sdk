"""
Grid Services module
"""
import json
import logging
import pprint

import requests


def service_restart(self, **kwargs) -> None:
    """
    restart services of group(s), member(s) or all

    :param self: WAPI class instance

    :param kwargs: method arguments

    :return None:
    """
    data = {}
    for prop, value in kwargs.items():
        if value:
            data[prop] = value
        elif prop == 'services':
            data[prop] = ['ALL']

    logging.debug(pprint.pformat(data))

    try:
        res = self.conn.post(
            f'{self.url}/{self.grid_ref}?_function=restartservices',
            json.dumps(data),
            verify=self.ssl_verify
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
    """
    Update the grid service restart status

    :param self: WAPI instance

    :param services: service(s) to check

    :return None:
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
    """
    Get and print table of all member service restart statuses

    :param self: WAPI instance

    :return service status (dict)
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
