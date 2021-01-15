import os
import typing as tp

from aiohttp import ClientSession

PORT = os.environ.get("BACK_END_PORT")
HOST = "back-end"  # os.environ.get("BACK_END_HOST")
PROTOCOL = os.environ.get("PROTOCOL", "http")
BASE_URL = f"{PROTOCOL}://{HOST}:{PORT}/api"


class Client:

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = ClientSession()

    def get(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return self.session.get(f"{self.base_url}/{method}", *args, **kwargs)

    def post(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return self.session.post(f"{self.base_url}/{method}", *args, **kwargs)

    def patch(self, method: str, *args: tp.Any, **kwargs: tp.Any) -> tp.Any:
        return self.session.patch(f"{self.base_url}/{method}", *args, **kwargs)


client = Client()
