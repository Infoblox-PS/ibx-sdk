#!/usr/bin/env python3
import getpass
import sys

import click

from infoblox_pslib.nios.wapi import WAPI, WapiRequestException
from infoblox_pslib.util.ibx_logger import (
    init_logger, increase_log_level
)

log = init_logger(
    logfile_name='wapi.log',
    logfile_mode='w',
    console_log=True,
    level='info'
)
wapi = WAPI()


def get_grid() -> dict:
    try:
        res = wapi.conn.get(f'{wapi.url}/grid', verify=wapi.ssl_verify)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(255)
    return res.json()[0]


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
    '-g', '--gm', required=True, help='Infoblox Grid Manager'
)
@click.option(
    '-w', '--wapi-ver', default='2.11', show_default=True,
    help="Infoblox WAPI version"
)
@click.option(
    '--debug', is_flag=True, help='enable verbose debug output'
)
def main(**args):
    if args.get('debug'):
        increase_log_level()
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
        sys.exit(255)

    grid = get_grid()
    log.info(grid)

    sys.exit()


if __name__ == '__main__':
    main()
