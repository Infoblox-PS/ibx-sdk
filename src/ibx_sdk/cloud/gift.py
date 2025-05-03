"""
gift.py

Infoblox Gift client module.

Provides:
  - A wrapper for Infoblox Cloud Swagger/OpenAPI metadata discovery and caching.
  - Helper methods to resolve endpoints and perform authenticated HTTP calls.
  - Per-user caching of the downloaded API specification.

Example:

    from gift import Gift

    # Initialize client (first run will fetch metadata)
    with Gift(api_key="YOUR_TOKEN", load_live=False) as client:
        # Fetch or read cached API spec
        api_paths = client.fetch_url_paths()

        # List endpoints for a specific API
        endpoints = client.find_endpoints(api_name="NTPService")
        for endpoint in endpoints:
            print(endpoint)

        # Make a GET call against a discovered endpoint
        response = client.get("service/config/mo6u4czggsvhsuxqmvzloqh7thjnc4si")
        print(response.json())
"""

import json
import logging
import asyncio
import os
from pathlib import Path
import re
from typing import Dict, List, Tuple, Optional

import httpx
import appdirs
from ibx_sdk.cloud.exceptions import ApiInvalidParameterException, ApiRequestException
from ibx_sdk.util.swagger_utils import build_swagger_index, fetch_swagger_json, API_NAMES

class Gift:
    """
    Infoblox Cloud API helper using Swagger metadata.

    Downloads the OpenAPI spec once (or on demand), caches it per-user,
    and provides methods to resolve and call endpoints dynamically.

    Attributes:
        api_key: CSP API token for Authorization header.
        base_path: Base URL for CSP API.
        load_live: If True, always refresh the cache on fetch.
        _cache_path: Filesystem path to the cached spec JSON.
        api_data: Endpoint metadata loaded from cache or network.
        url_map: Mapping of paths to method-specific endpoint metadata.
        session: HTTP client for making API calls.
    """

    def __init__(
        self,
        api_key: str,
        api_spec_file: str = os.environ.get("INFOBLOX_API_SPEC_FILE", "ibx_cloud_api_map.json"),
        load_live: bool = False,
        base_path: str = os.environ.get("INFOBLOX_BASE_PATH", "https://csp.infoblox.com"),
        extra_api_data: Optional[Dict] = None,
    ) -> None:
        """
        Initialize the Gift client.

        Args:
            api_key: CSP API token for Authorization header.
            api_spec_file: Filename or full path for the cached API specification.
            load_live: Force re-download of the spec if True.
            base_path: Base CSP URL (e.g., "https://csp.infoblox.com").
            extra_api_data: Additional endpoint definitions to merge into api_data.

        Example:
            >>> client = Gift(api_key="YOUR_TOKEN", load_live=False)
            >>> client.connect()
            >>> response = client.get("locations")
        """
        self.api_key = api_key
        self.base_path = base_path.rstrip("/")
        self.load_live = load_live
        self.session: Optional[httpx.Client] = None

        # Ensure cache lives in OS cache dir if no directory was provided
        cache = Path(api_spec_file)
        if cache.parent == Path('.'):
            cache_dir = Path(appdirs.user_cache_dir("com.infoblox.ibx-sdk", "Infoblox Professional Services"))
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache = cache_dir / cache.name
        self._cache_path = cache

        # Load or fetch API data
        if self.load_live or not self._cache_path.exists():
            self.api_data = asyncio.run(build_swagger_index(self.base_path, API_NAMES))
            with open(self._cache_path, "w", encoding="utf-8") as f:
                json.dump(self.api_data, f, indent=2)
        else:
            with open(self._cache_path, encoding="utf-8") as f:
                self.api_data = json.load(f)

        if extra_api_data:
            self.api_data.update(extra_api_data)

        self.url_map = self._build_url_map()

    def _build_url_map(self) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        Build a mapping from paths to endpoint entries, indexed by method.

        Returns:
            Mapping of normalized paths to method-specific metadata entries.

        Example:
            {
                "service/config": {
                    "GET": [{"method": "GET", "full_url": "...", "template": "...", "regex": ...}],
                    "POST": [...]
                }
            }
        """
        url_map: Dict[str, Dict[str, List[Dict[str, str]]]] = {}
        for key, meta in self.api_data.items():
            s_path = meta["s_path"].lstrip("/").rstrip("/")
            l_path = meta["l_path"].lstrip("/").rstrip("/")
            # Collect all parameters and assign unique group names
            params = re.findall(r"\{([^}]+)\}", l_path)
            param_counts = {}
            param_map = {}
            group_names = []
            for param in params:
                # Sanitize parameter name (replace '.' with '_')
                sanitized = param.replace('.', '_')
                # Handle duplicates by appending a numeric suffix
                param_counts[sanitized] = param_counts.get(sanitized, 0) + 1
                group_name = f"{sanitized}_{param_counts[sanitized]}" if param_counts[sanitized] > 1 else sanitized
                group_names.append(group_name)
                param_map[group_name] = param
            # Build regex pattern with unique group names
            pattern_parts = re.split(r"\{[^}]+\}", l_path)
            pattern = "^" + "".join(
                pattern_parts[i] + (f"(?P<{group_names[i]}>[^/]+)" if i < len(group_names) else "")
                for i in range(len(pattern_parts))
            ) + "$"
            entry = {
                "method": meta["method"],
                "full_url": f"{meta['base_url']}/{meta['l_path'].lstrip('/')}",
                "template": l_path,
                "key": key,
                "regex": re.compile(pattern) if "{" in l_path else None,
                "param_map": param_map
            }
            if s_path not in url_map:
                url_map[s_path] = {}
            if meta["method"] not in url_map[s_path]:
                url_map[s_path][meta["method"]] = []
            url_map[s_path][meta["method"]].append(entry)
            if s_path != l_path:
                if l_path not in url_map:
                    url_map[l_path] = {}
                if meta["method"] not in url_map[l_path]:
                    url_map[l_path][meta["method"]] = []
                url_map[l_path][meta["method"]].append(entry)
        return url_map

    def _normalize_path(self, path: str) -> str:
        """
        Normalize a path by removing leading/trailing slashes.

        Args:
            path: Input path to normalize (e.g., "/path/" or "path/to/resource").

        Returns:
            Normalized path string (e.g., "path" or "path/to/resource").
        """
        return path.lstrip("/").rstrip("/")

    def _resolve_endpoint(self, path: str, method: str) -> Tuple[str, Dict[str, str], Optional[Dict[str, str]]]:
        """
        Resolve a path to an endpoint, handling both short and literal paths.

        Args:
            path: The input path (e.g., "service/config" or "service/config/mo6u4czggsvhsuxqmvzloqh7thjnc4si").
            method: HTTP method (e.g., "GET").

        Returns:
            Tuple of (full URL, endpoint metadata, path parameters if any).

        Raises:
            ApiInvalidParameterException: If no matching endpoint is found.

        Example:
            >>> client._resolve_endpoint("service/config/abc123", "GET")
            ('https://csp.infoblox.com/api/ntp/v1/service/config/abc123', {...}, {'id': 'abc123'})
        """
        normalized_path = self._normalize_path(path)
        method = method.upper()
        logging.debug(f"Resolving endpoint for path: {normalized_path}, method: {method}")

        # Try exact match
        if normalized_path in self.url_map and method in self.url_map[normalized_path]:
            entries = self.url_map[normalized_path][method]
            logging.debug(f"Found exact match: {entries[0]['full_url']}")
            return entries[0]["full_url"], entries[0], None

        # Try suffix match
        for key, method_map in self.url_map.items():
            if normalized_path.endswith(key) and method in method_map:
                entries = method_map[method]
                logging.debug(f"Found suffix match: {entries[0]['full_url']}")
                return entries[0]["full_url"], entries[0], None

        # Try templated path match
        for key, method_map in self.url_map.items():
            if method not in method_map:
                continue
            for entry in method_map[method]:
                if entry["regex"]:
                    m = entry["regex"].match(normalized_path)
                    if m:
                        # Map sanitized group names back to original parameter names
                        path_params = {entry["param_map"].get(k, k): v for k, v in m.groupdict().items()}
                        full_url = entry["full_url"].format(**path_params)
                        logging.debug(f"Matched template {entry['template']} with params {path_params}, URL: {full_url}")
                        return full_url, entry, path_params

        logging.error(f"No endpoint found for path '{normalized_path}' and method '{method}'")
        raise ApiInvalidParameterException(f"No {method} endpoint for '{path}'")

    def fetch_url_paths(self) -> Dict[str, Dict]:
        """
        Fetch or load cached API specification.

        Returns:
            Dictionary of endpoint metadata.

        Example:
            >>> paths = client.fetch_url_paths()
            >>> print(paths.keys())
            ['NTPService GET /service/config/{id}', ...]
        """
        if not self.load_live and self._cache_path.exists():
            try:
                with open(self._cache_path, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        data = asyncio.run(build_swagger_index(self.base_path, API_NAMES))
        if self.load_live or not self._cache_path.exists():
            with open(self._cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        return data

    def get_all_endpoints(self) -> List[Dict[str, str]]:
        """
        List every discovered endpoint from the API specification.

        Returns:
            List of dictionaries with 'method', 'path', 'full_url', 'summary', and 'api'.

        Example:
            >>> endpoints = client.get_all_endpoints()
            >>> for ep in endpoints:
            ...     print(f"{ep['method']} {ep['path']}: {ep['summary']}")
        """
        endpoints = []
        for key, meta in self.api_data.items():
            endpoints.append({
                "method": meta["method"],
                "path": meta["l_path"],
                "full_url": f"{meta['base_url']}{meta['l_path']}",
                "summary": meta["summary"],
                "api": meta["api"]
            })
        return sorted(endpoints, key=lambda x: (x["api"], x["method"], x["path"]))

    def find_endpoints(
        self,
        api_name: Optional[str] = None,
        method: Optional[str] = None,
        path_contains: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Find endpoints matching specified criteria.

        Args:
            api_name: Filter by API component name (e.g., "NTPService").
            method: Filter by HTTP method (e.g., "GET").
            path_contains: Filter by substring in path (e.g., "service/config").

        Returns:
            List of endpoint metadata dictionaries with 'method', 'path', 'full_url', 'summary', and 'api'.

        Example:
            >>> endpoints = client.find_endpoints(api_name="NTPService", path_contains="service/config")
            >>> for ep in endpoints:
            ...     print(ep['path'])
        """
        endpoints = []
        for key, meta in self.api_data.items():
            if api_name and meta["api"] != api_name:
                continue
            if method and meta["method"] != method.upper():
                continue
            if path_contains and path_contains not in meta["l_path"]:
                continue
            endpoints.append({
                "method": meta["method"],
                "path": meta["l_path"],
                "full_url": f"{meta['base_url']}{meta['l_path']}",
                "summary": meta["summary"],
                "api": meta["api"]
            })
        return sorted(endpoints, key=lambda x: (x["api"], x["method"], x["path"]))

    def get_endpoint_parameters(self, path: str, method: str) -> List[Dict[str, str]]:
        """
        Retrieve query parameter metadata for an endpoint.

        Args:
            path: Endpoint path (e.g., "service/config/{id}").
            method: HTTP method (e.g., "GET").

        Returns:
            List of parameter metadata dictionaries with 'name', 'required', 'type', and 'description'.

        Example:
            >>> params = client.get_endpoint_parameters("service/config/{id}", "GET")
            >>> for param in params:
            ...     print(f"Parameter: {param['name']}, Required: {param['required']}")
        """
        normalized_path = self._normalize_path(path)
        method = method.upper()
        parameters = []

        for key, meta in self.api_data.items():
            if meta["method"] != method or not (meta["l_path"].lstrip("/") == normalized_path or meta["s_path"].lstrip("/") == normalized_path):
                continue
            swagger = asyncio.run(fetch_swagger_json(meta["api"], self.base_path))[1]
            if not swagger:
                continue
            for p, methods in swagger.get("paths", {}).items():
                if p != meta["l_path"]:
                    continue
                for m, details in methods.items():
                    if m.upper() != method:
                        continue
                    for param in details.get("parameters", []):
                        if param.get("in") == "query":
                            parameters.append({
                                "name": param["name"],
                                "required": param.get("required", False),
                                "type": param.get("type", "string"),
                                "description": param.get("description", "")
                            })
        return parameters

    def connect(self) -> None:
        """
        Establish an HTTP session with the required Authorization header.

        Raises:
            RuntimeError: If session is already established.

        Example:
            >>> client = Gift(api_key="YOUR_TOKEN")
            >>> client.connect()
        """
        if self.session:
            raise RuntimeError("Session already established.")
        self.session = httpx.Client(headers={"Authorization": f"Token {self.api_key}"})
        logging.debug("HTTP session established")

    def close(self) -> None:
        """
        Close the HTTP session.

        Example:
            >>> client.close()
        """
        if self.session:
            self.session.close()
            self.session = None
            logging.debug("HTTP session closed")

    def __enter__(self):
        """
        Enter context, establish session.

        Returns:
            Self for use in context manager.

        Example:
            >>> with Gift(api_key="YOUR_TOKEN") as client:
            ...     response = client.get("locations")
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context, close session."""
        self.close()

    def _call(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Execute an HTTP request against a resolved endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client request.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If session is not established via connect().
            ApiInvalidParameterException: If no matching endpoint found.
            ApiRequestException: On HTTP or request errors.

        Example:
            >>> response = client._call("GET", "locations", params={"_limit": 10})
            >>> print(response.json())
        """
        if not self.session:
            raise RuntimeError("Must call connect() before making API calls.")

        full_url, _, _ = self._resolve_endpoint(path, method)
        func = getattr(self.session, method.lower())
        logging.debug(f"Calling {method} {full_url} with kwargs: {kwargs}")

        try:
            response = func(full_url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            raise ApiRequestException(f"[{e.response.status_code}] {path}: {e.response.text}")
        except httpx.RequestError as e:
            raise ApiRequestException(f"Request failed for {path}: {e}")

    def get(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP GET to the resolved endpoint.

        Args:
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client.get(), such as params, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.

        Example:
            >>> client = Gift(api_key="YOUR_TOKEN")
            >>> client.connect()
            >>> response = client.get("locations", params={"_limit": 10})
            >>> print(response.json())
        """
        return self._call("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP POST to the resolved endpoint.

        Args:
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client.post(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.

        Example:
            >>> response = client.post("locations", json={"name": "New Location"})
            >>> print(response.json())
        """
        return self._call("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP PUT to the resolved endpoint.

        Args:
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client.put(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP PATCH to the resolved endpoint.

        Args:
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client.patch(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP DELETE to the resolved endpoint.

        Args:
            path: Endpoint path (e.g., "locations" or "service/config/abc123").
            **kwargs: Additional arguments passed to httpx.Client.delete(), such as headers or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("DELETE", path, **kwargs)

    def get_paginated(
        self,
        path: str,
        limit: int = 5000,
        fields: Optional[List[str]] = None,
        d_filter: Optional[str] = None,
        order_by: Optional[str] = None,
        tfilter: Optional[str] = None,
        torder_by: Optional[str] = None,
        page_token: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Fetch resources using pagination options.

        Args:
            path: Endpoint path to fetch (e.g., "locations").
            limit: Maximum number of items per page (default: 5000).
            fields: List of fields to return.
            d_filter: Filter expression for data.
            order_by: Sort order for results.
            tfilter: Nested filter expression.
            torder_by: Nested sort order.
            page_token: Pagination token for continuation.
            **kwargs: Additional request parameters (e.g., headers).

        Returns:
            List of result dictionaries aggregated across pages.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiInvalidParameterException: If the endpoint or method is not found.
            ApiRequestException: If the HTTP request fails.

        Example:
            >>> results = client.get_paginated("locations", limit=100, fields=["id", "name"])
            >>> for result in results:
            ...     print(result)
        """
        offset = 0
        results: List[Dict] = []

        while True:
            params = kwargs.pop("params", {})
            params.update({"_limit": limit, "_offset": offset})
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

            response = self.get(path, params=params)
            data = response.json()
            page_items = data.get("result") or data.get("results") or []
            if not page_items:
                break
            results.extend(page_items)
            if len(page_items) < limit:
                break
            offset += limit

        return results