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

import asyncio
import getpass
import sys
from typing import Literal

import click
from click_option_group import optgroup

from ibx_sdk.logger.ibx_logger import init_logger, increase_log_level
from ibx_sdk.nios.exceptions import WapiRequestException
from ibx_sdk.nios.asynchronous.gift import AsyncGift

log = init_logger(
    logfile_name="wapi.log",
    logfile_mode="a",
    console_log=True,
    level="info",
    max_size=100000,
    num_logs=1,
)

wapi = AsyncGift()


class LogType(click.ParamType):
    name = "log_type"
    log_types = [
        "SYSLOG",
        "AUDITLOG",
        "MSMGMTLOG",
        "DELTALOG",
        "OUTBOUND",
        "PTOPLOG",
        "DISCOVERY_CSV_ERRLOG",
    ]

    def convert(self, value, param, ctx):
        if value.upper() in self.log_types:
            return value.upper()
        self.fail(f"{value} is not a valid log type")


help_text = """
Get NIOS Log from Member
"""


def validate_rotated_logs(ctx, param, value):
    """
    Args:
        ctx: A Click context object containing information about the current invocation of the
        command.
        param: The Click parameter object being validated.
        value: The value passed to the parameter being validated.

    """
    log_type = ctx.params.get("log_type")
    if value and log_type != "SYSLOG":
        raise click.BadParameter(
            "--rotated-logs can only be set when --log-type is SYSLOG"
        )
    return value


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
    "-m", "--member", required=True, help="Member to retrieve log from"
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
    "-t",
    "--log-type",
    default="SYSLOG",
    type=LogType(),
    show_default=True,
    help="select log type",
)
@optgroup.option(
    "-n",
    "--node-type",
    type=click.Choice(["ACTIVE", "PASSIVE"]),
    default="ACTIVE",
    show_default=True,
    help="Node: ACTIVE | PASSIVE",
)
@optgroup.option(
    "-r",
    "--rotated-logs",
    is_flag=True,
    help="Include Rotated Logs",
    callback=validate_rotated_logs,
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
async def main(
    grid_mgr: str,
    member: str,
    username: str,
    log_type: Literal[str],
    node_type: Literal[str],
    rotated_logs: bool,
    wapi_ver: str,
    debug: bool,
) -> None:
    """
    Get NIOS Log from Member.

    Args:
        debug (bool): If True, it sets the log level to DEBUG. Default is False.
        grid_mgr (str): Manager for the wapi grid.
        member (str): Grid Member
        username (str): Username for the wapi connection.
        log_type (Literal[str]): Log type
        node_type (Literal[str]) Node Type [ ACTIVE | PASSIVE ]
        wapi_ver (str): Version of wapi.
        rotated_logs (bool):

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
        await wapi.connect(username=username, password=password)
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)
    else:
        log.info("connected to Infoblox grid manager %s", wapi.grid_mgr)

    try:
        await wapi.get_log_files(
            member=member,
            log_type=log_type,
            node_type=node_type,
            include_rotated=rotated_logs,
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info("finished!")
    sys.exit()


if __name__ == "__main__":
    asyncio.run(main())
