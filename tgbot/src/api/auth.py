import typing as tp

from collections import namedtuple

from aiohttp import ClientResponse

from api.client import client

from utils.auth import check_token
# ------------------------------------------------------------------------------

Session = namedtuple("Session", ["id", "code", "chat_id"])


@check_token
async def fetch_session(params: dict[str, tp.Any]) -> tp.Optional[Session]:
    """Fetch session for chat. Session may not exist, hence `Optional`."""

    async with client.get("tgbot/session", params=params) as response:
        data: list[dict[str, tp.Any]] = await response.json()

    return Session(**data[0]) if data else None


async def session_exists(chat_id: int) -> bool:
    """Determine whether session for chat exists."""

    session = await fetch_session(params={"chat_id": chat_id})
    exists = session and session.chat_id == chat_id
    return exists


async def fetch_code(chat_id: int) -> str:
    """Fetch code for **authorized** user.

    Contract: session must exist.
    """

    session = await fetch_session(params={"chat_id": chat_id})
    assert session is not None

    return session.code


async def patch_session(id_: int, data: dict[str, tp.Any]) -> ClientResponse:
    """Patch some fields of session."""

    async with client.patch(f"tgbot/session/{id_}/", json=data) as response:
        return response


# ------------------------------------------------------------------------------

AuthorizeResult = namedtuple("AuthorizeResult", ["success", "details"])


async def authorize(chat_id: int, code: str) -> AuthorizeResult:
    """Link chat with session using code."""

    session = await fetch_session(params={"code": code})

    if session is None:
        return AuthorizeResult(success=False, details="Несуществующий код")

    if session.chat_id is not None:
        return AuthorizeResult(success=False, details="Код уже используется")

    response = await patch_session(session.id, data={"chat_id": chat_id})
    if response.status // 100 != 2:
        details = f"Ошибка сервиса авторизации: {response.reason}"
        return AuthorizeResult(success=False, details=details)

    return AuthorizeResult(success=True, details="")


DeauthorizeResult = namedtuple("DeauthorizeResult", ["success", "details"])


async def deauthorize(chat_id: int) -> DeauthorizeResult:
    """Unlink chat from session."""

    session = await fetch_session(params={"chat_id": chat_id})
    if session is None or session.chat_id is None:
        return DeauthorizeResult(success=True, details="")

    response = await patch_session(session.id, data={"chat_id": None})
    if response.status // 100 != 2:
        details = f"Ошибка сервиса авторизации: {response.reason}"
        return DeauthorizeResult(success=False, details=details)

    return DeauthorizeResult(success=True, details="")


# ------------------------------------------------------------------------------

User = namedtuple("User", ["full_name", "milgroup"])


async def fetch_user(chat_id: int) -> User:
    return User(full_name="ФИО", milgroup="1809")
