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
import pprint
from typing import Literal, Optional

import requests

ServiceRestartMode = Literal['GROUPED', 'SEQUENTIAL', 'SIMULTANEOUS']
ServiceRestartOption = Literal['FORCE_RESTART', 'RESTART_IF_NEEDED']
ServiceRestartServices = Literal['ALL', 'DNS', 'DHCP', 'DHCPV4', 'DHCPV6']


class NiosServiceMixin:
    """
    NIOS Service Mixin class
    """

    def service_restart(
            self,
            groups: Optional[list] = None,
            members: Optional[list[str]] = None,
            mode: Optional[ServiceRestartMode] = None,
            restart_option: Optional[ServiceRestartOption] = 'RESTART_IF_NEEDED',
            services: Optional[list[ServiceRestartServices]] = None,
            user_name: Optional[str] = None,
    ) -> None:
        data = {}
        if groups:
            data['groups'] = [groups]
        if members:
            data['members'] = [members]
        if mode:
            data['mode'] = mode
        if restart_option:
            data['restart_option'] = restart_option
        if services:
            data['services'] = [services]
        if user_name:
            data['user_name'] = user_name

        logging.debug(pprint.pformat(data))

        try:
            res = self.post(
                self.grid_ref, params={'_function': 'restartservices'}, json=data
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise
        else:
            logging.info(
                'successfully restarted %s services', data.get('services')
            )

    def update_service_status(self, services: str = 'ALL') -> None:
        payload = {'service_option': services}
        try:
            res = self.post(
                self.grid_ref, params={'_function': 'requestrestartservicestatus'}, json=payload
            )
            logging.debug(res.text)
            res.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.error(err)
            raise

    def get_service_restart_status(self) -> dict:
        try:
            response = self.get('restartservicestatus')
            logging.debug(response.text)
            response.raise_for_status()
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
            return response.json()
