#!/usr/bin/env python3
import getpass
import sys
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


def delete_record(_ref):
    res = wapi.delete(
        f'{wapi.url}/{_ref}',
        verify=wapi.ssl_verify
    )
    return res.json()


def create_record():
    res = wapi.post(
        f'{wapi.url}/record:a',
        data={'name': 'api-record-test.example.com', 'ipv4addr': '10.10.10.10'},
        verify=wapi.ssl_verify
    )
    return res.json()


def update_record(_ref):
    res = wapi.put(
        f'{wapi.url}/{_ref}',
        data={'comment': 'update the comment'},
        verify=wapi.ssl_verify
    )
    return res.json()


def get_record() -> dict:
    res = wapi.get(
        f'{wapi.url}/record:a', params={'name': 'api-record-test.example.com'},
        verify=wapi.ssl_verify
    )
    return res.json()


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
    wapi.connect()

    # check if record exists
    log.info('checking if record:a exists')
    res = get_record()
    log.info(res)

    # create record
    log.info('creating record:a object')
    res = create_record()
    log.info(res)

    # get record
    log.info('checking if record:a was created')
    res = get_record()
    log.info(res)

    # update record
    log.info('updating record:a using %s', res[0].get('_ref'))
    res = update_record(res[0].get('_ref'))
    log.info(res)

    # get record
    log.info('fetching updated record:a object')
    res = get_record()
    log.info(res)

    # delete record
    log.info('removing record:a from the database')
    res = delete_record(res[0].get('_ref'))
    log.info(res)

    sys.exit()


if __name__ == '__main__':
    main()
