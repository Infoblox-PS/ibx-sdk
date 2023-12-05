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
@optgroup.option('-s', '--server', required=True, help="Infoblox NIOS Grid Manager IP/Hostname")
@optgroup.option('-f', '--filename', required=True, help="Infoblox NIOS Grid restore filename")
@optgroup.group("\nOptional Parameters")
@optgroup.option('-u', '--username', show_default=True, help="Infoblox NIOS username")
@optgroup.option('-p', '--password', prompt=True, hide_input=True, help="Infoblox NIOS password")
@optgroup.option('-m', '--mode', type=click.Choice(["NORMAL", "FORCED", "CLONE"], case_sensitive=True),
                 default="FORCED", show_default=True, help="Grid Restore Mode [NORMAL|FORCED|CLONE]")
@optgroup.option('-k', '--keep', is_flag=True, help="Keep existing IP otherwise use IP from backup")
@optgroup.option('-w', '--wapi-ver', default='2.11', show_default=True, help='Infoblox WAPI version')
@optgroup.group("\nLogging Parameters")
@optgroup.option('--debug', is_flag=True, help="Enable verbose logging")
@click.version_option(__version__)
def main(server: str, username: str, filename: str, mode: str, keep: bool,
         debug: bool, wapi_ver: str) -> None:
    """
     Restore NIOS Grid.

     Args:
         server (str): Infoblox NIOS Grid Manager IP/Hostname (Required).
         username (str): Infoblox NIOS username (Optional, default='admin').
         filename (str): Infoblox NIOS Grid restore filename (Required).
         mode (str): Grid Restore Mode [NORMAL|FORCED|CLONE] (Optional, default="FORCED").
         keep (bool): Keep existing IP otherwise use IP from backup (Optional).
         debug (bool): Enable verbose logging (Optional).
         wapi_ver (str): Version of wapi.

     Returns:
         None

     Raises:
         Any exceptions raised during the process.
     """
    sys.tracebacklimit = 0
    if debug:
        increase_log_level()
        sys.tracebacklimit = 1

    # MISC
    wapi.wapi_ver = wapi_ver
    wapi.username = username
    wapi.password = getpass.getpass(
        f'Enter password for [{wapi.username}]: '
    )
    wapi.grid_mgr = server
    wapi.ssl_verify = False

    wapi.connect()

    wapi.grid_restore(
        filename=filename,
        mode=mode,
        keep_grid_ip=keep,
    )


if __name__ == "__main__":
    # execute only if run as a script
    main()
