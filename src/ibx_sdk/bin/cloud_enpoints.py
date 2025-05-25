#!/usr/bin/env python3
"""
Utility CLI to print all Infoblox Cloud API endpoints or URL map.
"""
import click
from ibx_sdk.cloud.gift import Gift


@click.command()
@click.option(
    "--api-spec-file", default="infoblox_api_calls.json", show_default=True,
    help="Path to the Swagger index JSON file."
)
@click.option(
    "--base-path", default="https://csp.infoblox.com", show_default=True,
    help="Base URL for the API."
)
@click.option(
    "--live", is_flag=True, default=False,
    help="Fetch the latest Swagger index remotely."
)
@click.option(
    "--url-map", "show_map", is_flag=True, default=False,
    help="Print the short-path to full URL mappings instead of raw endpoints."
)
def main(api_spec_file, base_path, live, show_map):
    """
    Print all Infoblox Cloud API endpoints or URL map using the Gift wrapper methods.
    """
    # Instantiate Gift without an API key, since we're only listing
    g = Gift(
        api_key=None,
        api_spec_file=api_spec_file,
        load_live=live,
        base_path=base_path
    )

    endpoints = g.get_all_endpoints()

    if show_map:
        endpoints = g.get_all_endpoints()

        for m in endpoints:
            click.echo(f"{m['method']} {m['path']} → {m['full_url']}")
    else:
        endpoints = g.get_all_endpoints()
        for ep in endpoints:
            click.echo(f"{ep['method']} {ep['path']} → {ep['full_url']}")


if __name__ == "__main__":
    main()
