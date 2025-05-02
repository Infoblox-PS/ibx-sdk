import json
import time
import os
import asyncio
import httpx

from ibx_sdk.cloud.exceptions import ( ApiInvalidParameterException, ApiRequestException)

API_NAMES = [
    "BootstrapApp", "Infrastructure", "Locations", "NIOSXasaService", "NTPService",
    "HostActivation", "Anycast", "Authz", "Identity", "Notifications-Thresholding",
    "Atcfw", "Atcep", "Atcdfp", "Redirect", "Scheduler",
    "Ipamsvc", "DnsConfig", "DhcpLeases", "DDIKeys",
    "ThirdPartyProviders", "CloudDiscoveryProviders", "CloudForwarders", "IpamFederation"
]

class APIError(Exception):
    """Custom API error that mimics httpx.HTTPStatusError, but simplified."""
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code

async def fetch_swagger_json(api_name: str, base_url: str):
    """Fetch Swagger/OpenAPI JSON for a given API component."""
    url = f"{base_url}/apidoc/docs/{api_name}?format=openapi"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return api_name, response.json()
    except Exception:
        return api_name, None

def extract_endpoints(api_name, swagger_json):
    """Extract endpoint definitions from Swagger JSON into a flat dictionary."""
    endpoints = {}
    if not swagger_json:
        return endpoints

    host = swagger_json.get("host", "csp.infoblox.com")
    base_path = swagger_json.get("basePath", "").rstrip("/")
    base_url = f"https://{host}{base_path}"

    paths = swagger_json.get("paths", {})
    for path, methods in paths.items():
        s_path = path.split("{")[0].rstrip("/") if "{" in path else path
        for method, details in methods.items():
            key = f"{api_name} {method.upper()} {path}"
            endpoints[key] = {
                "api": api_name,
                "method": method.upper(),
                "l_path": path,
                "s_path": s_path,
                "summary": details.get("summary", ""),
                "operation_id": details.get("operationId", ""),
                "base_url": base_url
            }
    return endpoints

async def build_swagger_index(base_path: str):
    """Build a full API endpoint index from all Swagger components."""
    results = await asyncio.gather(*(fetch_swagger_json(name, base_path) for name in API_NAMES))
    api_dict = {}
    for api_name, swagger_json in results:
        api_dict.update(extract_endpoints(api_name, swagger_json))
    return api_dict

class Gift:
    """
    A simple Infoblox Cloud API wrapper using Swagger metadata for endpoint resolution.

    Args:
        api_key (str): Infoblox API token.
        api_spec_file (str): Path to a cached Swagger JSON index file.
        load_live (bool): If True, fetch Swagger metadata at runtime.
        base_path (str): The base URL for Infoblox API (default: https://csp.infoblox.com)
        extra_api_data (dict): Optional additional endpoint definitions to merge in.
    """
    def __init__(
        self,
        api_key: str = None,
        api_spec_file: str = "infoblox_api_calls.json",
        load_live: bool = False,
        base_path: str = "https://csp.infoblox.com",
        extra_api_data: dict | None = None,
    ):
        self.api_key = api_key
        self.session = None
        self.base_path = base_path

        # load or fetch the swagger index
        if load_live or not os.path.exists(api_spec_file):
            self.api_data = asyncio.run(build_swagger_index(base_path))
            with open(api_spec_file, "w") as f:
                json.dump(self.api_data, f, indent=2)
        else:
            with open(api_spec_file) as f:
                self.api_data = json.load(f)

        # merge in any extra definitions passed by the user
        if extra_api_data:
            # extra_api_data should be a dict of key -> endpoint-dict
            self.api_data.update(extra_api_data)

        # ...then build your url_map as before
        self.url_map = self._build_url_map()

    def _build_url_map(self) -> dict:
        """Construct a mapping of short paths to full endpoint metadata."""
        url_map = {}
        for entry in self.api_data.values():
            s_path_key = entry["s_path"]
            method = entry["method"]
            base_url = entry["base_url"]
            full_url = f"{base_url}{entry['l_path']}"
            url_map.setdefault(s_path_key, []).append({
                "method": method,
                "full_url": full_url
            })
        return url_map

    def connect(self):
        """Establish an HTTPX session with authorization headers."""
        self.session = httpx.Client(headers={"Authorization": f"Token {self.api_key}"})

    def _resolve_path(self, short_path: str) -> list:
        """Resolve a simplified path key to matching endpoint candidates."""
        if short_path in self.url_map:
            return self.url_map[short_path]
        matches = [v for k, v in self.url_map.items() if k.endswith(f"/{short_path}")]
        if matches:
            return matches[0]
        available = ", ".join(sorted(self.url_map.keys()))
        raise ValueError(f"No matching endpoint found for '{short_path}'. Available keys: {available}")

    def _call(self, method: str, short_path: str, **kwargs) -> httpx.Response:
        candidates = self._resolve_path(short_path)
        for entry in candidates:
            if entry["method"] != method:
                continue

            request_fn = getattr(self.session, method.lower())
            url = entry["full_url"]

            retries = 3
            backoff = 1.0
            for attempt in range(1, retries + 1):
                try:
                    # Handle body/json logic
                    if "json" in kwargs:
                        response = request_fn(url, **kwargs)
                    elif method in {"POST", "PUT", "PATCH"}:
                        response = request_fn(url, **kwargs)
                    else:
                        params = kwargs.pop("params", {})
                        for key in ("_fields", "_filter", "_order_by", "_torder_by"):
                            if key in kwargs:
                                params[key] = kwargs.pop(key)
                        response = request_fn(url, params=params, **kwargs)

                    response.raise_for_status()
                    return response

                except httpx.HTTPStatusError as e:
                    if e.response.status_code in {502, 503, 504} and attempt < retries:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                    raise ApiRequestException(
                        f"[{e.response.status_code}] {short_path} failed: {e.response.text}"
                    ) from e

                except httpx.RequestError as e:
                    if attempt < retries:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                    raise ApiRequestException(
                        f"Request error on '{short_path}': {str(e)}"
                    ) from e

        raise ApiInvalidParameterException(f"No {method} method available for '{short_path}'")

    def get(self, short_path: str, **kwargs) -> httpx.Response:
        """Perform a GET request on the resolved endpoint."""
        return self._call("GET", short_path, **kwargs)

    def post(self, short_path: str, **kwargs) -> httpx.Response:
        """Perform a POST request on the resolved endpoint."""
        return self._call("POST", short_path, **kwargs)

    def put(self, short_path: str, **kwargs) -> httpx.Response:
        """Perform a PUT request on the resolved endpoint."""
        return self._call("PUT", short_path, **kwargs)

    def patch(self, short_path: str, **kwargs) -> httpx.Response:
        """Perform a PATCH request on the resolved endpoint."""
        return self._call("PATCH", short_path, **kwargs)

    def delete(self, short_path: str, **kwargs) -> httpx.Response:
        """Perform a DELETE request on the resolved endpoint."""
        return self._call("DELETE", short_path, **kwargs)

    def list_available_paths(self, method: str = "GET") -> list[str]:
        """Return available endpoint short paths filtered by HTTP method."""
        return sorted(
            k for k, v in self.url_map.items()
            if any(entry["method"] == method.upper() for entry in v)
        )

    def get_paginated(
        self,
        short_path: str,
        limit: int = 5000,
        fields: list[str] = None,
        d_filter: str = None,
        order_by: str = None,
        tfilter: str = None,
        torder_by: str = None,
        page_token: str = None,
        **kwargs
    ) -> list:
        """Perform a paginated GET request using Infoblox Cloud query options."""
        offset = 0
        results = []

        while True:
            params = kwargs.get("params", {})
            params["_limit"] = limit
            params["_offset"] = offset
            if fields:
                params["_fields"] = ",".join(fields)
            if d_filter:
                params["_filter"] = d_filter
            if order_by:
                params["_order_by"] = order_by
            if tfilter:
                params["_tfilter"] = tfilter
            if torder_by:
                params["_torder_by"] = torder_by
            if page_token:
                params["_page_token"] = page_token

            kwargs["params"] = params
            response = self.get(short_path, **kwargs)

            try:
                data = response.json()
            except Exception:
                break

            items = data.get("result") or data.get("results") or []
            if not items:
                break

            results.extend(items)

            if len(items) < limit:
                break
            offset += limit

        return results
