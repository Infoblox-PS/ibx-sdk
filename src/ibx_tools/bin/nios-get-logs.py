#!/usr/bin/env python3
import getpass
import sys

import click
from click_option_group import optgroup

from ibx_tools.logger.ibx_logger import init_logger, set_log_level
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
Retrieve Log from NIOS Member
"""


@click.command(help=help_text, context_settings=dict(max_content_width=95, help_option_names=['-h', '--help']))
@optgroup.group("Required Parameters")
@optgroup.option('-g', '--grid-mgr', required=True, help='Infoblox Grid Manager')
@optgroup.option('-m', '--member', required=True, help='Member to retrieve log from')
@optgroup.group("Optional Parameters")
@optgroup.option('-u', '--username', default='admin', show_default=True, help='Infoblox admin username')
@optgroup.option('-t', '--log-type', default='SYSLOG',
                 show_default=True, help='SYSLOG | AUDITLOG | MSMGMTLOG |'
                                         'DELTALOG | OUTBOUND | PTOPLOG |'
                                         'DISCOVERY_CSV_ERRLOG]')
@optgroup.option('-n', '--node-type', type=click.Choice(["ACTIVE", "PASSIVE"]), default='ACTIVE',
                 show_default=True, help='Node: ACTIVE | PASSIVE')
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("Logging Parameters")
@optgroup.option('--debug', is_flag=True, help='enable verbose debug output')
def main(**args):
    """
    The main driver function which sets up the wapi configuration, connects to Infoblox grid manager
    and fetches the log files from members.

    Args:
        **args: Arbitrary keyword arguments.
            debug (bool): If True, it sets the log level to DEBUG. Default is False.
            grid-mgr (str): Manager for the wapi grid.
            member (str): Grid Member
            username (str): Username for the wapi connection.
            log-type (str): Log type
            node-type (str) Node Type [ ACTIVE | PASSIVE ]
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
    member = args.get('member')
    log_type = args.get('log_type')
    node = args.get('node_type')
    try:
        wapi.connect()
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    log.info('connected to Infoblox grid manager %s', wapi.grid_mgr)
    wapi.get_log_files(member=member, log_type=log_type, node_type=node)
    log.info('finished!')
    sys.exit()


if __name__ == '__main__':
    main()
