import logging
import ssl
from typing import Union, Optional

import httpx

from ibx_sdk.nios.asynchronous.fileop import NiosFileopMixin
from ibx_sdk.nios.exceptions import (
    WapiInvalidParameterException,
    WapiRequestException,
)
from ibx_sdk.nios.service import NiosServiceMixin


class AsyncGift(httpx.AsyncClient, NiosServiceMixin, NiosFileopMixin):
    def __init__(
        self,
        grid_mgr: str = None,
        wapi_ver: str = "2.5",
        ssl_verify: Union[bool, str] = False,
    ):
        self.grid_mgr = grid_mgr
        self.wapi_ver = wapi_ver
        self.ssl_verify = ssl_verify
        self.conn = None
        self.grid_ref = None
        super().__init__()

    def __repr__(self):
        args = []
        for key, value in self.__dict__.items():
            args.append(f"{key}={value}")
        return f"{self.__class__.__qualname__}({', '.join(args)})"

    @property
    def url(self) -> str:
        return (
            f"https://{self.grid_mgr}/wapi/v{self.wapi_ver}"
            if self.grid_mgr and self.wapi_ver
            else ""
        )

    async def connect(
        self,
        username: str = None,
        password: str = None,
        certificate: str = None,
    ):
        if not self.url:
            logging.error("invalid url %s - unable to connect!", self.url)
            raise WapiInvalidParameterException

        if username and password:
            await self.__basic_auth_request(username, password)
        elif certificate:
            await self.__certificate_auth_request(certificate)
        else:
            raise WapiInvalidParameterException

    async def __basic_auth_request(self, username: str, password: str):
        auth = httpx.BasicAuth(username, password)
        ctx = ssl.create_default_context()
        if self.ssl_verify:
            ctx.load_verify_locations(cafile=self.ssl_verify)
        else:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        try:
            self.conn = httpx.AsyncClient(auth=auth, verify=ctx)
            res = await self.conn.get(f"{self.url}/grid")
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            raise WapiRequestException(exc) from exc
        else:
            grid = res.json()
            self.grid_ref = grid[0].get("_ref")

    async def __certificate_auth_request(self, certificate: str):
        ctx = ssl.create_default_context()
        ctx.load_cert_chain(certfile=certificate)
        if self.ssl_verify:
            ctx.load_verify_locations(cafile=self.ssl_verify)
        else:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        try:
            self.conn = httpx.AsyncClient(verify=ctx)
            res = await self.conn.get(f"{self.url}/grid")
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            raise WapiRequestException(exc) from exc
        else:
            grid = res.json()
            self.grid_ref = grid[0].get("_ref")

    async def get(
        self, wapi_object: str, params: Optional[dict] = None, **kwargs
    ) -> httpx.Response:
        res = await self.conn.get(
            f"{self.url}/{wapi_object}", params=params, **kwargs
        )
        res.raise_for_status()
        return res

    async def getone(
        self, wapi_object: str, params: Optional[dict] = None, **kwargs
    ) -> str:
        res = await self.conn.get(
            f"{self.url}/{wapi_object}", params=params, **kwargs
        )
        res.raise_for_status()
        data = res.json()
        if len(data) != 1:
            raise WapiRequestException("Expected exactly one result")
        return data[0].get("_ref", "")

    async def post(
        self, wapi_object: str, json: Optional[dict] = None, **kwargs
    ) -> httpx.Response:
        res = await self.conn.post(
            f"{self.url}/{wapi_object}", json=json, **kwargs
        )
        res.raise_for_status()
        return res

    async def put(
        self,
        wapi_object_ref: str,
        data: Optional[Union[dict, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        res = await self.conn.put(
            f"{self.url}/{wapi_object_ref}", data=data, **kwargs
        )
        res.raise_for_status()
        return res

    async def delete(self, wapi_object_ref: str, **kwargs) -> httpx.Response:
        res = await self.conn.delete(f"{self.url}/{wapi_object_ref}", **kwargs)
        res.raise_for_status()
        return res

    async def object_fields(self, wapi_object: str) -> Union[str, None]:
        try:
            res = await self.conn.get(f"{self.url}/{wapi_object}?_schema")
            res.raise_for_status()
            data = res.json()
        except httpx.HTTPStatusError as exc:
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            raise WapiRequestException(exc) from exc
        else:
            fields = ",".join(
                field["name"]
                for field in data.get("fields")
                if "r" in field.get("supports")
            )
        return fields

    async def max_wapi_ver(self) -> None:
        url = f"https://{self.grid_mgr}/wapi/v1.0/?_schema"
        try:
            res = await self.conn.get(url)
            res.raise_for_status()
            data = res.json()
        except httpx.HTTPStatusError as exc:
            raise WapiRequestException(exc) from exc
        except httpx.RequestError as exc:
            raise WapiRequestException(exc) from exc
        else:
            versions = data.get("supported_versions")
            versions.sort(key=lambda s: list(map(int, s.split("."))))
            max_wapi_ver = versions.pop()
            setattr(self, "wapi_ver", max_wapi_ver)
