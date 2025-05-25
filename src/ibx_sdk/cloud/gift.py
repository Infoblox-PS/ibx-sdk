"""
gift.py

Infoblox Gift client module.

Provides:
  - A simplified way to make authenticated HTTP calls to the Infoblox Cloud API using full paths.

Example:

    from gift import Gift

    # Initialize client with base_url
    with Gift(api_key="YOUR_TOKEN", base_url="https://csp.infoblox.com") as client:
        # Make a GET call with the full path
        response = client.get("/api/ddi/v1/dns/view")
        print(response.json())

Additional Examples:

    # Initialize with a custom base_url
    client = Gift(api_key="YOUR_TOKEN", base_url="https://custom.api.example.com")
    client.connect()
    response = client.get("/api/ddi/v1/dns/view")
    print(response.json())
    client.close()

    # Use context manager for automatic session management
    with Gift(api_key="YOUR_TOKEN") as client:
        response = client.get("/api/ddi/v1/dns/view")
        print(response.json())

    # Make a POST request with JSON data
    with Gift(api_key="YOUR_TOKEN") as client:
        data = {"name": "New View", "description": "A new DNS view"}
        response = client.post("/api/ddi/v1/dns/view", json=data)
        print(response.json())

    # Handle paginated responses
    with Gift(api_key="YOUR_TOKEN") as client:
        results = client.get_paginated("/api/ddi/v1/ipam/subnet", limit=50)
        print(f"Total subnets: {len(results)}")
        for subnet in results:
            print(subnet)

    # Use filters and fields in paginated requests
    with Gift(api_key="YOUR_TOKEN") as client:
        fields = ["id", "name"]
        d_filter = "name=='default'"
        results = client.get_paginated("/api/ddi/v1/dns/view", limit=10, fields=fields, d_filter=d_filter)
        for view in results:
            print(view)

    # Handle errors
    with Gift(api_key="INVALID_TOKEN") as client:
        try:
            response = client.get("/api/ddi/v1/invalid/path")
        except ApiRequestException as e:
            print(f"API request failed: {e}")
"""

import logging
from typing import List, Dict, Optional

import httpx
from ..cloud.exceptions import ApiRequestException

class Gift:
    """
    Infoblox Cloud API helper for direct path usage.

    Attributes:
        api_key: CSP API token for Authorization header.
        base_url: Base URL for CSP API (e.g., "https://csp.infoblox.com").
        session: HTTP client for making API calls.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://csp.infoblox.com",
    ) -> None:
        """
        Initialize the Gift client.

        Args:
            api_key: CSP API token for Authorization header.
            base_url: Base CSP URL (e.g., "https://csp.infoblox.com").

        Example:
            >>> client = Gift(api_key="YOUR_TOKEN", base_url="https://custom.api.example.com")
            >>> client.connect()
            >>> response = client.get("/api/ddi/v1/dns/view")
            >>> print(response.json())
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session: Optional[httpx.Client] = None

    def connect(self) -> None:
        """
        Establish an HTTP session with the required Authorization header.

        Raises:
            RuntimeError: If session is already established.

        Example:
            >>> client = Gift(api_key="YOUR_TOKEN", base_url="https://csp.infoblox.com")
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
            ...     response = client.get("/api/ddi/v1/dns/view")
            ...     print(response.json())
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context, close session."""
        self.close()

    def _call(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Execute an HTTP request against the provided full path.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client request.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If session is not established via connect().
            ApiRequestException: On HTTP or request errors.
        """
        if not self.session:
            raise RuntimeError("Must call connect() before making API calls.")

        full_url = f"{self.base_url}{path}"
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
        Perform an HTTP GET to the provided full path.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client.get(), such as params, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiRequestException: If the HTTP request fails.

        Example:
            >>> with Gift(api_key="YOUR_TOKEN") as client:
            ...     response = client.get("/api/ddi/v1/dns/view")
            ...     print(response.json())
        """
        return self._call("GET", path, **kwargs)

    def get_paginated(
            self,
            path: str,
            limit: int = 100,
            fields: Optional[List[str]] = None,
            d_filter: Optional[str] = None,
            **kwargs
    ) -> List[Dict]:
        """
        Fetch all pages of resources from the API using pagination.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/ipam/subnet").
            limit: Maximum number of records per page (default: 100).
            fields: List of fields to return (optional).
            d_filter: Filter expression for data (optional).
            **kwargs: Additional arguments passed to the get() method.

        Returns:
            A list of all collected results from the paginated responses.

        Raises:
            ApiRequestException: If any API request fails.

        Example:
            >>> with Gift(api_key="YOUR_TOKEN") as client:
            ...     results = client.get_paginated("/api/ddi/v1/ipam/subnet", limit=50)
            ...     print(f"Total subnets: {len(results)}")
            ...     for subnet in results:
            ...         print(subnet)
        """
        results = []
        offset = 0

        while True:
            params = kwargs.get('params', {})
            params['_limit'] = limit
            params['_offset'] = offset
            if fields:
                params['_fields'] = ','.join(fields)
            if d_filter:
                params['_filter'] = d_filter

            response = self.get(path, params=params)
            data = response.json()

            if 'results' in data:
                page_results = data['results']
            elif 'result' in data:
                page_results = data['result']
            else:
                page_results = data

            if not isinstance(page_results, list):
                break

            results.extend(page_results)

            if len(page_results) < limit:
                break

            offset += limit

        return results

    def post(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP POST to the provided full path.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client.post(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiRequestException: If the HTTP request fails.

        Example:
            >>> with Gift(api_key="YOUR_TOKEN") as client:
            ...     data = {"name": "New View", "description": "A new DNS view"}
            ...     response = client.post("/api/ddi/v1/dns/view", json=data)
            ...     print(response.json())
        """
        return self._call("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP PUT to the provided full path.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client.put(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP PATCH to the provided full path.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client.patch(), such as json, headers, or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        """
        Perform an HTTP DELETE to the provided full path.

        Args:
            path: Full API path (e.g., "/api/ddi/v1/dns/view").
            **kwargs: Additional arguments passed to httpx.Client.delete(), such as headers or timeout.

        Returns:
            httpx.Response: The HTTP response object.

        Raises:
            RuntimeError: If connect() has not been called.
            ApiRequestException: If the HTTP request fails.
        """
        return self._call("DELETE", path, **kwargs)