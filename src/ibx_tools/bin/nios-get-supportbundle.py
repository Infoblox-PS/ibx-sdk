#!/usr/bin/env python3
import getpass
import sys

import click

from ibx_tools.logger.ibx_logger import init_logger, set_log_level
from ibx_tools.nios.wapi import WAPI, WapiRequestException

log = init_logger(
    logfile_name='nios-get-supportbundle.log',
    logfile_mode='w',
    level='info',
    console_log=True,
)
wapi = WAPI()


@click.command(
    context_settings=dict(
        max_content_width=90,
        help_option_names=['-h', '--help']
    )
)
@click.option(
    '-u', '--username', default='admin', show_default=True,
    help='Infoblox admin username'
)
@click.option(
    '-g', '--grid-mgr', default='192.168.1.2', show_default=True, help='Infoblox Grid Manager'
)
@click.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help="Infoblox WAPI version"
)
@click.option(
    '--debug', is_flag=True, help='enable verbose debug output'
)
def main(**args):
    """
    The main driver function which sets up the wapi configuration, connects to the Infoblox grid manager,
    and initiates a support bundle request for a specific Infoblox member.

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it sets the log level to DEBUG. Default is False.
            gm (str): Manager for the wapi grid.
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.

    Returns:
        None

    Raises:
        WapiRequestException: If unable to connect with the provided wapi parameters.
        SystemExit: The function exits the system upon completion or upon encounter of an error.

    """
    if args.get('debug', False):
        set_log_level('DEBUG', 'both')

    wapi.grid_mgr = args.get('grid_mgr')
    wapi.username = args.get('username')
    wapi.wapi_ver = args.get('wapi_ver')
    wapi.password = getpass.getpass(
        f'Enter password for [{wapi.username}]: '
    )
    try:
        wapi.connect()
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info('connected to Infoblox grid manager %s', wapi.grid_mgr)
    wapi.get_support_bundle(member='infoblox.localdomain')
    log.info('finished!')
    sys.exit()


if __name__ == '__main__':
    main()
