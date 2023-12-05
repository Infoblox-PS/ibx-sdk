#!/usr/bin/env python3
import getpass
import sys
from typing import Union

import click
from infoblox_pslib.nios.wapi import WAPI
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


def get_object_properties(wapi_object: str) -> Union[str, None]:
    res = wapi.object_fields(wapi_object)
    return res


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
    '-o', '--object', required=True, help='Infoblox WAPI Object'
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
    wapi_object = args.get('object')
    wapi.connect()

    # check if record exists
    log.info('fetching all properties for %s', wapi_object)
    res = get_object_properties(wapi_object)
    log.info(res)

    sys.exit()


if __name__ == '__main__':
    main()
