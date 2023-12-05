#!/usr/bin/env python3
import getpass
import sys

import click
from click_option_group import optgroup

from ibx_tools.logger.ibx_logger import init_logger, increase_log_level
from ibx_tools.nios.wapi import WAPI, WapiRequestException

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='a',
    console_log=True,
    level='info',
    max_size=10000,
    num_logs=1)

wapi = WAPI()

help_text = """
Retrieve Support Bundle from Member
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help='Infoblox Grid Manager')
@optgroup.option('-m', '--member', required=True, help='Member to retrieve log from')
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', default='admin', show_default=True, help='Infoblox admin username')
@optgroup.option('-r', '--rotated-logs', default=True, show_default=True, help='Include Rotated Logs')
@optgroup.option('-l', '--logs-files', default=True, show_default=True, help='Include Log Files')
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help='enable verbose debug output')
def main(**args):
    """
    The main driver function which sets up the wapi configuration, connects to the Infoblox grid manager,
    and initiates a support bundle request for a specific Infoblox member.

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it sets the log level to DEBUG. Default is False.
            grid-mgr (str): Manager for the wapi grid.
            member (str): Grid Member
            username (str): Username for the wapi connection.
            wapi_ver (str): Version of wapi.

    Returns:
        None

    Raises:
        WapiRequestException: If unable to connect with the provided wapi parameters.
        SystemExit: The function exits the system upon completion or upon encounter of an error.

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
    try:
        wapi.connect()
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    member = args.get('member')
    rotated = args.get('rotated_logs')
    logs = args.get('log_files')

    log.info('connected to Infoblox grid manager %s', wapi.grid_mgr)
    wapi.get_support_bundle(member=member,
                            log_files=logs,
                            nm_snmp_logs=False,
                            recursive_cache_file=False,
                            remote_url=None,
                            rotate_log_files=rotated)

    log.info('finished!')
    sys.exit()


if __name__ == '__main__':
    main()
