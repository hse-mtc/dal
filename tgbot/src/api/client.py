import os
import typing as tp

from aiohttp import ClientSession

PORT = os.environ.get("BACK_END_PORT")
BASE_URL = f"http://back-end:{PORT}/api/tgbot"


class Client:

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = ClientSession()

    def get(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return self.session.get(f"{self.base_url}/{method}", *args, **kwargs)

    def patch(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return self.session.patch(f"{self.base_url}/{method}", *args, **kwargs)


client = Client()
