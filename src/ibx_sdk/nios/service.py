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

import httpx
from ibx_sdk.nios.exceptions import WapiRequestException


class NiosServiceMixin:
    """
    NIOS Service Mixin class
    """

    RestartMode = Literal["GROUPED", "SEQUENTIAL", "SIMULTANEOUS"]
    RestartOption = Literal["FORCE_RESTART", "RESTART_IF_NEEDED"]
    RestartServices = Literal["ALL", "DNS", "DHCP", "DHCPV4", "DHCPV6"]

    def service_restart(
        self,
        groups: Optional[list] = None,
        members: Optional[list[str]] = None,
        mode: Optional[RestartMode] = None,
        restart_option: Optional[RestartOption] = "RESTART_IF_NEEDED",
        services: Optional[list[RestartServices]] = None,
        user_name: Optional[str] = None,
    ) -> None:
        """
        Restarts specified services on the grid.

        Args:
            self (Gift): Gift object
            groups (Optional[list]): List of group names. Default is None.
            members (Optional[list[str]]): List of member names. Default is None.
            mode (Optional[ServiceRestartMode]): Restart mode. Default is None.
            restart_option (Optional[ServiceRestartOption]): Restart option. The default is
                            'RESTART_IF_NEEDED'.
            services (Optional[list[ServiceRestartServices]]): List of services to restart.
                                                               Default is None.
            user_name (Optional[str]): Username. Default is None.

        Returns:
            None

        Raises:
            httpx.RequestError: If there is an error, send the restart request.

        Examples:
            # Restart services in a group
            service_restart(groups=['group_name'])

            # Restart services of specific members
            service_restart(members=['member1', 'member2'])

            # Restart services with a specific restart mode
            service_restart(mode=ServiceRestartMode.IMMEDIATE)

            # Restart services with a specific restart option
            service_restart(restart_option=ServiceRestartOption.RESTART_IF_NEEDED)

            # Restart specific services
            service_restart(services=[ServiceRestartServices.SERVICE_NAME1,
            ServiceRestartServices.SERVICE_NAME2])

            # Restart services for a specific user
            service_restart(user_name='username')
        """
        data = {}
        if groups:
            data["groups"] = [groups]
        if members:
            data["members"] = [members]
        if mode:
            data["mode"] = mode
        if restart_option:
            data["restart_option"] = restart_option
        if services:
            data["services"] = [services]
        if user_name:
            data["user_name"] = user_name

        logging.debug(pprint.pformat(data))

        try:
            res = self.post(
                self.grid_ref,
                params={"_function": "restartservices"},
                json=data,
            )
            res.raise_for_status()
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc
        else:
            logging.info(
                "successfully restarted %s services", data.get("services")
            )

    def update_service_status(self, services: str = "ALL") -> None:
        """
        Updates the status of a service.

        Args:
            self (Gift): The instance of the class.
            services (str): The service option to update the status for.
                            The default value is 'ALL'.

        Returns:
            None

        Raises:
            httpx.RequestError: If an error occurs while making the request.
        """
        payload = {"service_option": services}
        try:
            res = self.post(
                self.grid_ref,
                params={"_function": "requestrestartservicestatus"},
                json=payload,
            )
            res.raise_for_status()
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc

    def get_service_restart_status(self) -> dict:
        """
        Retrieves the status of a service restart.

        Args:
            self (Gift): The instance of the Gift class

        Returns:
            dict: A dictionary containing the service restart status information.

        Raises:
            httpx.RequestError: If there is a general request error.
        """
        try:
            response = self.get("restartservicestatus")
            response.raise_for_status()
            try:
                return response.json()
            except httpx.DecodingError as exc:
                logging.error(f"DecodingError: {exc}")
                raise WapiRequestException(response.text) from exc
        except httpx.TimeoutException as exc:
            logging.error(f"Timeout error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error: {exc}")
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            logging.error(f"Request error: {exc}")
            raise WapiRequestException(exc) from exc
