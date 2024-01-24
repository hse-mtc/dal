import os
import typing as tp

from aiohttp import ClientSession

from config import (
    TGBOT_EMAIL,
    TGBOT_PASSWORD,
)

PORT = os.environ.get("BACK_END_PORT")
HOST = "back-end"  # os.environ.get("BACK_END_HOST")
PROTOCOL = os.environ.get("PROTOCOL", "http")
BASE_URL = f"{PROTOCOL}://{HOST}:{PORT}/api"


class Client:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = None
        self.auth_headers: dict[str, str] = {}

    async def _do_request(
        self,
        verb: str,
        method: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Any:
        # Initialize session first if needed.
        if self.session is None:
            self.session = ClientSession()

        # Get provided headers, if any.
        headers: dict[str, tp.Any] = kwargs.pop("headers", {})
        # Add auth headers.
        headers.update(self.auth_headers)
        # Put headers back to `kwargs`.
        kwargs["headers"] = headers

        # Send request.
        url = f"{self.base_url}/{method}"
        call_me = getattr(self.session, verb)
        response = await call_me(url, *args, **kwargs)

        # No authorization errors, proceed as usual.
        if response.status != 401:
            return response

        # Request failed because of authorization.
        # Obtain new access and refresh tokens.
        await self._refresh_auth()

        # Try again.
        return await self._do_request(verb, method, *args, **kwargs)

    async def _refresh_auth(self) -> None:
        body = {"email": TGBOT_EMAIL, "password": TGBOT_PASSWORD}
        response = await self.post("auth/tokens/obtain/", json=body)
        tokens = await response.json()
        access = tokens["access"]
        self.auth_headers = {"Authorization": f"Bearer {access}"}

    async def get(
        self,
        method: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Any:
        return await self._do_request("get", method, *args, **kwargs)

    async def post(
        self,
        method: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Any:
        return await self._do_request("post", method, *args, **kwargs)

    async def patch(
        self,
        method: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Any:
        return await self._do_request("patch", method, *args, **kwargs)

    async def delete(
        self,
        method: str,
        *args: tp.Any,
        **kwargs: tp.Any,
    ) -> tp.Any:
        return await self._do_request("delete", method, *args, **kwargs)


client = Client()
