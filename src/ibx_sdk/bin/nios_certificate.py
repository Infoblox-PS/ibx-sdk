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
ALGORITHMS = click.Choice(["SHA-256", "SHA-384", "SHA-512"])
USAGES = click.Choice(
    ["ADMIN", "CAPTIVE_PORTAL", "SFNT_CLIENT_CERT", "IFMAP_DHCP"]
)
ALL_USAGES = click.Choice(
    [
        "ADMIN",
        "CAPTIVE_PORTAL",
        "SFNT_CLIENT_CERT",
        "IFMAP_DHCP",
        "EAP_CA",
        "TAE_CA",
    ]
)
wapi = Gift()
help_text = """
NIOS SSL Certificate Tools
"""


@click.group(
    help=help_text,
    context_settings=dict(
        max_content_width=95,
        help_option_names=["-h", "--help"],
        show_default=True,
    ),
)
def cli():
    pass


@cli.command()
@optgroup.group("Required Parameters")
@optgroup.option(
    "-g", "--grid-mgr", required=True, help="Infoblox Grid Manager"
)
@optgroup.option(
    "-m", "--member", required=True, help="Member for the certificate"
)
@optgroup.option(
    "-f",
    "--filename",
    required=True,
    help="Upload filename for the certificate",
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "--certificate-usage",
    default="ADMIN",
    type=ALL_USAGES,
    help="Certificate Usage",
)
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.11",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.option("--debug", is_flag=True, help="enable verbose debug output")
def upload(
    grid_mgr: str,
    member: str,
    filename: str,
    username: str,
    wapi_ver: str,
    certificate_usage: str,
    debug: bool,
):
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
        wapi.upload_certificate(
            member=member,
            filename=filename,
            certificate_usage=certificate_usage,
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info("finished!")
    sys.exit()


@cli.command()
@optgroup.group("Required Parameters")
@optgroup.option(
    "-g", "--grid-mgr", required=True, help="Infoblox Grid Manager"
)
@optgroup.option(
    "-m", "--member", required=True, help="Member for the certificate"
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "--certificate-usage",
    default="ADMIN",
    type=ALL_USAGES,
    help="Certificate Usage",
)
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.11",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.option("--debug", is_flag=True, help="enable verbose debug output")
def download(
    grid_mgr: str,
    member: str,
    username: str,
    wapi_ver: str,
    certificate_usage: str,
    debug: bool,
):
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
        wapi.download_certificate(
            member=member, certificate_usage=certificate_usage
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info("finished!")
    sys.exit()


@cli.command()
@optgroup.group("Required Parameters")
@optgroup.option(
    "-g", "--grid-mgr", required=True, help="Infoblox Grid Manager"
)
@optgroup.option(
    "-n", "--common-name", required=True, help="Common Name for the certificate"
)
@optgroup.option(
    "-m", "--member", required=True, help="Member for the certificate"
)
@optgroup.option(
    "-d",
    "--days-valid",
    default=365,
    help="Number of days the certificate is valid for",
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.11",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.group("Optional Certificate Parameters")
@optgroup.option(
    "-a",
    "--algorithm",
    default="SHA-256",
    type=ALGORITHMS,
    help="The digest algorithm",
)
@optgroup.option(
    "--certificate-usage",
    default="ADMIN",
    type=USAGES,
    help="Certificate Usage",
)
@optgroup.option("-c", "--comment", help="Certificate comment")
@optgroup.option("--country", default="US", help="Certificate country")
@optgroup.option("-e", "--email", help="Certificate email address")
@optgroup.option("-k", "--key-size", default=2048, help="Certificate key size")
@optgroup.option("-l", "--locality", help="Certificate locality")
@optgroup.option("-o", "--organization", help="Certificate organization")
@optgroup.option("--ou", help="Certificate organizational unit")
@optgroup.option("-s", "--state", help="Certificate state")
@optgroup.option(
    "--san", help="Certificate subject alternative name(s) as [TYPE/VALUE,...]"
)
@optgroup.group("Logging Parameters")
@optgroup.option("--debug", is_flag=True, help="enable verbose debug output")
def selfsign(
    grid_mgr: str,
    common_name: str,
    member: str,
    days_valid: int,
    username: str,
    wapi_ver: str,
    algorithm: str,
    certificate_usage: str,
    comment: str,
    country: str,
    email: str,
    key_size: int,
    locality: str,
    organization: str,
    ou: str,
    state: str,
    san: str,
    debug: bool,
):
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

    subject_alt_names = san.split(",") if san else None
    if subject_alt_names:
        new_list = []
        for san in subject_alt_names:
            san_type, san_value = san.split("/")
            if san_type not in ["DNS", "IP", "URI", "EMAIL"]:
                log.error(f"Invalid subject alternative name type: {san_type}")
                sys.exit(1)
            new_list.append({"type": san_type, "value": san_value})
        subject_alt_names = new_list

    try:
        wapi.generate_selfsigned_cert(
            cn=common_name,
            member=member,
            days_valid=days_valid,
            algorithm=algorithm,
            certificate_usage=certificate_usage,
            comment=comment,
            country=country,
            email=email,
            key_size=key_size,
            locality=locality,
            org=organization,
            org_unit=ou,
            state=state,
            subject_alternative_names=subject_alt_names,
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info("finished!")
    sys.exit()


@cli.command()
@optgroup.group("Required Parameters")
@optgroup.option(
    "-g", "--grid-mgr", required=True, help="Infoblox Grid Manager"
)
@optgroup.option(
    "-n", "--common-name", required=True, help="Common Name for the certificate"
)
@optgroup.option(
    "-m", "--member", required=True, help="Member for the certificate"
)
@optgroup.group("Optional Parameters")
@optgroup.option(
    "-u",
    "--username",
    default="admin",
    help="Infoblox admin username",
)
@optgroup.option(
    "-w",
    "--wapi-ver",
    default="2.11",
    show_default=True,
    help="Infoblox WAPI version",
)
@optgroup.group("Optional Certificate Parameters")
@optgroup.option(
    "-a",
    "--algorithm",
    default="SHA-256",
    type=ALGORITHMS,
    help="The digest algorithm",
)
@optgroup.option(
    "--certificate-usage",
    default="ADMIN",
    type=USAGES,
    help="Certificate Usage",
)
@optgroup.option("-c", "--comment", help="Certificate comment")
@optgroup.option("--country", default="US", help="Certificate country")
@optgroup.option("-e", "--email", help="Certificate email address")
@optgroup.option("-k", "--key-size", default=2048, help="Certificate key size")
@optgroup.option("-l", "--locality", help="Certificate locality")
@optgroup.option("-o", "--organization", help="Certificate organization")
@optgroup.option("--ou", help="Certificate organizational unit")
@optgroup.option("-s", "--state", help="Certificate state")
@optgroup.option(
    "--san", help="Certificate subject alternative name(s) as [TYPE/VALUE,...]"
)
@optgroup.group("Logging Parameters")
@optgroup.option("--debug", is_flag=True, help="enable verbose debug output")
def gencsr(
    grid_mgr: str,
    common_name: str,
    member: str,
    username: str,
    wapi_ver: str,
    algorithm: str,
    certificate_usage: str,
    comment: str,
    country: str,
    email: str,
    key_size: int,
    locality: str,
    organization: str,
    ou: str,
    state: str,
    san: str,
    debug: bool,
) -> None:
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

    subject_alt_names = san.split(",") if san else None
    if subject_alt_names:
        new_list = []
        for san in subject_alt_names:
            san_type, san_value = san.split("/")
            if san_type not in ["DNS", "IP", "URI", "EMAIL"]:
                log.error(f"Invalid subject alternative name type: {san_type}")
                sys.exit(1)
            new_list.append({"type": san_type, "value": san_value})
        subject_alt_names = new_list

    try:
        wapi.generate_csr(
            cn=common_name,
            member=member,
            algorithm=algorithm,
            certificate_usage=certificate_usage,
            comment=comment,
            country=country,
            email=email,
            key_size=key_size,
            locality=locality,
            org=organization,
            org_unit=ou,
            state=state,
            subject_alternative_names=subject_alt_names,
        )
    except WapiRequestException as err:
        log.error(err)
        sys.exit(1)

    log.info("finished!")
    sys.exit()


if __name__ == "__main__":
    cli()
