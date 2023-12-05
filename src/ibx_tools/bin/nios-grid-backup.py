#!/usr/bin/env python3
import getpass
import sys

import click

from ibx_tools.logger.ibx_logger import init_logger, increase_log_level
from ibx_tools.nios.wapi import WAPI

log = init_logger(
    logfile_name='nios-grid-backup.log',
    logfile_mode='w',
    console_log=True,
    level='info'
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
    '-g', '--grid-mgr', required=True, help='Infoblox Grid Manager'
)
@click.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help="Infoblox WAPI version"
)
@click.option(
    '-f', '--file', default='database.tgz', show_default=True,
    help='Infoblox backup file name'
)
@click.option(
    '--debug', is_flag=True, help='enable verbose debug output'
)
def main(**args):
    """
    The main driver function which sets up the wapi configuration, connects to the Infoblox grid
    manager and initiates a grid backup.

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it increases the logging level.
            gm (str): Manager for the wapi grid.
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.
            file (str): Filename/path where the backup will be saved.

    Returns:
        None

    Raises:
        Could raise various exceptions depending on the execution of internal functions.

    """
    if args.get('debug'):
        increase_log_level()
    wapi.grid_mgr = args.get('grid_mgr')
    wapi.username = args.get('username')
    wapi.wapi_ver = args.get('wapi_ver')
    wapi.password = getpass.getpass(
        f'Enter password for [{wapi.username}]: '
    )
    wapi.connect()

    wapi.grid_backup(filename=args.get('file'))

    sys.exit()


if __name__ == '__main__':
    main()
