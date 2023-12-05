#!/usr/bin/env python3
import getpass
import sys

import click

from ibx_tools.logger.ibx_logger import init_logger, set_log_level
from ibx_tools.nios.wapi import WAPI, WapiRequestException


log = init_logger(
    logfile_name='nios-log.log',
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
    '-g', '--gm', default='192.168.1.2', show_default=True, help='Infoblox Grid Manager'
)
@click.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help="Infoblox WAPI version"
)
@click.option(
    '--debug', is_flag=True, help='enable verbose debug output'
)
def main(**args):
    if args.get('debug', False):
        set_log_level('DEBUG', 'both')

    wapi.grid_mgr = args.get('gm')
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
    wapi.get_log_files(member='infoblox.localdomain', log_type='SYSLOG', node_type="ACTIVE")
    log.info('finished!')
    sys.exit()


if __name__ == '__main__':
    main()
