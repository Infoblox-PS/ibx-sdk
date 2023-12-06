#!/usr/bin/env python3
import getpass
import sys

import click
from click_option_group import optgroup

from ibx_tools.logger.ibx_logger import init_logger, increase_log_level
from ibx_tools.nios.wapi import WAPI

# from pkg_resources import parse_versio

__version__ = '2.0.0'

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='a',
    console_log=True,
    level='info',
    max_size=10000,
    num_logs=1)

wapi = WAPI()

help_text = """
Restore NIOS Grid.
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help="Infoblox NIOS Grid Manager IP/Hostname")
@optgroup.option('-f', '--filename', required=True, help="Infoblox NIOS Grid restore filename")
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', show_default=True, help="Infoblox NIOS username")
@optgroup.option('-m', '--mode', type=click.Choice(["NORMAL", "FORCED", "CLONE"], case_sensitive=True),
                 default="FORCED", show_default=True, help="Grid Restore Mode [NORMAL|FORCED|CLONE]")
@optgroup.option('-k', '--keep', is_flag=True, help="Keep existing IP otherwise use IP from backup")
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help="Enable verbose logging")
@click.version_option(__version__)
def main(**args):
    """
    Restore NIOS Grid

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it increases the logging level.
            grid-mgr (str): Manager for the wapi grid.
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.
            file (str): Filename/path where the backup will be saved.

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

    wapi.connect()

    wapi.grid_restore(
        filename=args.get('filename'),
        mode=args.get('mode'),
        keep_grid_ip=args.get('keep')
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
