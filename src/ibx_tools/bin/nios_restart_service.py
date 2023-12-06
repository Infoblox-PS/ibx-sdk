#!/usr/bin/env python3
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

import getpass
import sys

import click
from click_option_group import optgroup

from ibx_tools.logger.ibx_logger import init_logger, increase_log_level
from ibx_tools.nios.wapi import WAPI

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='a',
    console_log=True,
    level='info',
    max_size=100000,
    num_logs=1)

wapi = WAPI()

help_text = """
Restart NIOS Protocol Services
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help='Infoblox Grid Manager')
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', default='admin', show_default=True, help='Infoblox admin username')
@optgroup.option('-s', '--service', type=click.Choice(['DNS', 'DHCP', 'DHCPV4', 'DHCPV6', 'ALL']),
                 default='ALL', show_default=True, help='select which service to restart')
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help='enable verbose debug output')
def main(**args):
    """
    Restart NIOS Protocol Services

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it increases the logging level.
            grid_mgr (str): Manager for the wapi grid.
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.
            service (str): The service to be restarted.

    Notes:
        In the service restart method, either 'groups' or 'members' can be specified, but not both.

    Returns:
        None

    Raises:
        Could raise various exceptions depending on the execution of internal functions.

    """
    sys.tracebacklimit = 0
    if args.get('debug'):
        increase_log_level()
        sys.tracebacklimit = 1

    wapi.grid_mgr = args.get('grid_mgr')
    wapi.username = args.get('username')
    wapi.wapi_ver = args.get('wapi_ver')
    wapi.password = getpass.getpass(
        f'Enter password for [{wapi.username}]: '
    )
    wapi.connect()
    wapi.service_restart(
        # groups: [group1, ...],
        # or
        # members: [member1, member2, ...]
        mode='SEQUENTIAL',
        restart_option='RESTART_IF_NEEDED',
        services=[args.get('service')]
    )

    sys.exit()


if __name__ == '__main__':
    main()
