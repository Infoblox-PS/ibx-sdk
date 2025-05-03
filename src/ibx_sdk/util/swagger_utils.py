"""
swagger_utils.py

Utilities for fetching and processing Infoblox Cloud Swagger/OpenAPI specifications.
"""

import json
import logging
import asyncio
from typing import Dict, Optional, Tuple, List
import httpx

API_NAMES = [
    "BootstrapApp", "Infrastructure", "Locations", "NIOSXasaService", "NTPService",
    "HostActivation", "Anycast", "Authz", "Identity", "Notifications-Thresholding",
    "Atcfw", "Atcep", "Atcdfp", "Redirect", "Scheduler",
    "Ipamsvc", "DnsConfig", "DhcpLeases", "DDIKeys",
    "ThirdPartyProviders", "CloudDiscoveryProviders", "CloudForwarders", "IpamFederation"
]

async def fetch_swagger_json(api_name: str, base_url: str) -> Tuple[str, Optional[Dict]]:
    """
    Fetch Swagger/OpenAPI JSON for a component asynchronously.

    Args:
        api_name: Component name from API_NAMES.
        base_url: Base URL of the CSP API (e.g., https://csp.infoblox.com).

    Returns:
        A tuple of (component name, parsed JSON dict) or None if an error occurred.

    Example:
        >>> name, swagger = await fetch_swagger_json("NTPService", "https://csp.infoblox.com")
        >>> print(swagger.get("paths"))
    """
    url = f"{base_url}/apidoc/docs/{api_name}?format=openapi"
    logging.debug(f"Fetching Swagger JSON for {api_name} from {url}")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return api_name, response.json()
    except (httpx.HTTPStatusError, httpx.RequestError, json.JSONDecodeError) as e:
        logging.error(f"Error fetching {api_name}: {e}")
        return api_name, None

def extract_endpoints(api_name: str, swagger_json: Optional[Dict]) -> Dict[str, Dict]:
    """
    Extract endpoint definitions from Swagger JSON.

    Args:
        api_name: Name of the API component.
        swagger_json: Parsed Swagger/OpenAPI JSON.

    Returns:
        Mapping of "<ApiName> <METHOD> <path>" to metadata dict.

    Example:
        >>> endpoints = extract_endpoints("NTPService", swagger_json)
        >>> print(endpoints.keys())
        ['NTPService GET /service/config/{id}', ...]
    """
    endpoints: Dict[str, Dict] = {}
    if not swagger_json:
        return endpoints

    host = swagger_json.get("host", "csp.infoblox.com")
    base_path = swagger_json.get("basePath", "").rstrip("/")
    base_url = f"https://{host}{base_path}"

    for path, methods in swagger_json.get("paths", {}).items():
        clean_path = path.split("{")[0].rstrip("/") if "{" in path else path
        for method, details in methods.items():
            key = f"{api_name} {method.upper()} {path}"
            endpoints[key] = {
                "api": api_name,
                "method": method.upper(),
                "l_path": path,
                "s_path": clean_path,
                "summary": details.get("summary", ""),
                "operation_id": details.get("operationId", ""),
                "base_url": base_url
            }
    return endpoints

async def build_swagger_index(base_path: str, api_names: List[str]) -> Dict[str, Dict]:
    """
    Build a full API endpoint index by downloading all Swagger components.

    Args:
        base_path: CSP base URL.
        api_names: List of API component names to fetch.

    Returns:
        Combined endpoint metadata for all components.

    Example:
        >>> index = await build_swagger_index("https://csp.infoblox.com", API_NAMES)
        >>> print(len(index))
        200
    """
    tasks = [fetch_swagger_json(name, base_path) for name in api_names]
    results = await asyncio.gather(*tasks)
    api_dict: Dict[str, Dict] = {}
    for api_name, swagger in results:
        api_dict.update(extract_endpoints(api_name, swagger))
    return api_dict