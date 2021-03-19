import os
import typing as tp

from api.client import client


def check_token(request_method: tp.Awaitable):
    async def wrapper(*args: tp.Any, **kwargs: tp.Any):
        try:
            response = await request_method(*args, **kwargs)
        except:
            token = await fetch_token()
            headers = fetch_headers(token)
            response = await request_method(headers=headers, *args, **kwargs)
        return response
    return wrapper


async def fetch_token() -> str:
    body = {
        "username": os.environ["TGBOT_USERNAME"],
        "password": os.environ["TGBOT_PASSWORD"]
    }
    async with client.post("auth/tokens/obtain/", json=body) as resp:
        response = await resp.json()
    return response.get("access", None)


def fetch_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}"
    }
