#!/usr/bin/env python3
"""
Copyright 2023 Infoblox

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import getpass
import sys

import click
from click_option_group import optgroup

from ibx_sdk.logger.ibx_logger import init_logger, increase_log_level
from ibx_sdk.nios.exceptions import WapiRequestException
from ibx_sdk.nios.gift import Gift

log = init_logger(
    logfile_name="wapi.log",
    logfile_mode="a",
    console_log=True,
    level="info",
    max_size=100000,
    num_logs=1,
)

wapi = Gift()

help_text = """
CSV Import Data
"""


@click.command(
    help=help_text,
    context_settings=dict(
        max_content_width=95, help_option_names=["-h", "--help"]
    ),
)
@optgroup.group("Required Parameters")
@optgroup.option(
    "-g", "--grid-mgr", required=True, help="Infoblox Grid Manager"
)
@optgroup.option(
    "-f", "--filename", required=True, help="Infoblox WAPI CSV import file name"
)
@optgroup.option(
    "-o",
    "--operation",
    required=True,
    type=click.Choice(["INSERT", "OVERRIDE", "MERGE", "DELETE", "CUSTOM"]),
    help="CSV import mode",
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    show_default=True,
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.11",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.group("Logging Parameters")
@optgroup.option("--debug", is_flag=True, help="enable verbose debug output")
def main(
    grid_mgr: str,
    filename: str,
    operation: str,
    username: str,
    wapi_ver: str,
    debug: bool,
) -> None:
    """
    CSV Import

    Args:
        debug (bool): If True, it sets the log level to DEBUG. Default is False.
        grid_mgr (str): Manager for the wapi grid.
        username (str): Username for the wapi connection.
        wapi_ver (str): Version of wapi.
        operation (str): Operation to be performed on import.
        filename (str): Filename/path of csv file to be imported.

    Returns:
        None

    Raises:
        WapiRequestException: If unable to connect with the provided wapi parameters.
        SystemExit: The function exits the system upon completion or upon encounter of an error.

    """
    if debug:
        increase_log_level()

    wapi.grid_mgr = grid_mgr
    wapi.wapi_ver = wapi_ver
    password = getpass.getpass(f"Enter password for [{username}]: ")
    try:
        wapi.connect(username=username, password=password)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    else:
        log.info("connected to Infoblox grid manager %s", wapi.grid_mgr)

    try:
        wapi.csv_import(
            task_operation=operation,
            csv_import_file=filename,
            exit_on_error=False,
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    sys.exit()


if __name__ == "__main__":
    main()
