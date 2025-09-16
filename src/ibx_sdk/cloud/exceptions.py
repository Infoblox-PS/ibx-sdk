"""Exceptions module for Infoblox Cloud SDK

Defines a hierarchy of custom exceptions for robust error handling
and clear semantics when interacting with the Infoblox Cloud API.
"""

__all__ = [
    "BaseCloudException",
    "ApiInvalidParameterException",
    "ApiRequestException",
]

class BaseCloudException(Exception):
    """
    Base exception for all Infoblox Cloud SDK errors.

    Inherit from this class to create SDK-specific exceptions.
    """
    pass

class ApiInvalidParameterException(BaseCloudException):
    """
    Raised when invalid arguments or parameters are passed to SDK methods.

    Indicates that the caller provided bad input that the SDK cannot
    resolve into a valid API call (e.g., unknown resource path).
    """
    def __init__(self, message: str):
        super().__init__(f"Invalid parameter: {message}")
        self.message = message

class ApiRequestException(BaseCloudException):
    """
    Raised when an HTTP request to the Infoblox Cloud API fails.

    Captures HTTP errors, non-2xx responses, or API-level error payloads.

    Attributes:
        status_code (int | None): HTTP status code of the failed response.
        payload (Any | None): Parsed JSON payload if available.
    """
    def __init__(
        self,
        message: str,
        status_code: int = None,
        payload: object = None,
        original_exception: Exception = None,
    ):
        """
        Initialize the ApiRequestException.

        Args:
            message: Human-readable error description.
            status_code: HTTP status code, if applicable.
            payload: Parsed JSON payload returned by the API.
            original_exception: Underlying exception instance, for chaining.
        """
        full_msg = "Request failed"
        if status_code is not None:
            full_msg += f" [{status_code}]"
        full_msg += f": {message}"
        super().__init__(full_msg)
        self.status_code = status_code
        self.payload = payload
        # Chain original exception for traceback clarity
        if original_exception is not None:
            self.__cause__ = original_exception
