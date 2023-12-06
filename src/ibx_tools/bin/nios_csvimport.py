#!/usr/bin/env python3
import getpass
import sys

import click
from click_option_group import optgroup

from ibx_tools.logger.ibx_logger import (
    init_logger, increase_log_level
)
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
CSV Import Data
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help='Infoblox Grid Manager')
@optgroup.option('-f', '--file', required=True, help='Infoblox WAPI CSV import file name')
@optgroup.option('-o', '--operation', required=True,
                 type=click.Choice(['INSERT', 'OVERRIDE', 'MERGE', 'DELETE', 'CUSTOM']),
                 help='CSV import mode')
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', default='admin', show_default=True, help='Infoblox admin username')
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help='enable verbose debug output')
def main(**args):
    """
    CSV Import

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it increases the logging level.
            grid-mgr (str): Manager for the wapi grid.
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.
            operation (str): Operation to be performed on import.
            file (str): Filename/path of csv file to be imported.

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

    wapi.csv_import(
        task_operation=args.get('operation'),
        csv_import_file=args.get('file'),
        exit_on_error=False,
    )

    sys.exit()


if __name__ == '__main__':
    main()
