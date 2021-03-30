import os
import typing as tp

from functools import wraps

from api.client import client


RequestMethod = tp.Callable[..., tp.Awaitable]


def auth_required(request_method: RequestMethod):

    @wraps(request_method)
    async def wrapper(*args: tp.Any, **kwargs: tp.Any):
        try:
            response = await request_method(*args, **kwargs)
        except:
            token = await fetch_token()
            headers = make_headers(token)
            response = await request_method(headers=headers, *args, **kwargs)
        return response

    return wrapper


async def fetch_token() -> str:
    body = {
        "username": os.environ["TGBOT_USERNAME"],
        "password": os.environ["TGBOT_PASSWORD"],
    }

    async with client.post("auth/tokens/obtain/", json=body) as resp:
        response = await resp.json()

    return response["access"]


def make_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
    }
