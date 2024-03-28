class BaseWapiException(Exception):
    """BaseWapiException class"""


class WapiInvalidParameterException(BaseWapiException):
    """WapiInvalidParameterException class - raised when invalid args/params passed to methods"""


class WapiRequestException(BaseWapiException):
    """WapiRequestException class - returns error(s) returned from Infoblox WAPI calls"""

    def __init__(self, msg):
        super().__init__(f"wapi error - {msg}")
