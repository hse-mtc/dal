import typing as tp

from collections import namedtuple

from aiohttp import ClientResponse

from api.client import client
from api.student import fetch_students

# ------------------------------------------------------------------------------

Session = namedtuple("Session", ["id", "phone", "chat_id"])


async def fetch_session(
    params: dict[str, tp.Any],
    *args: tp.Any,
    **kwargs: tp.Any,
) -> tp.Optional[Session]:
    """Fetch session for chat. Session may not exist, hence `Optional`."""

    method = "tgbot/session/"
    response = await client.get(method, params=params, *args, **kwargs)
    data: list[dict[str, tp.Any]] = await response.json()
    return Session(**data[0]) if data else None


async def post_session(
    body: dict[str, tp.Any],
    *args: tp.Any,
    **kwargs: tp.Any,
) -> Session:
    """Create new session."""

    method = "tgbot/session/"
    response = await client.post(method, json=body, *args, **kwargs)
    data: dict[str, tp.Any] = await response.json()
    return Session(**data)


async def patch_session(
    id_: int,
    data: dict[str, tp.Any],
    *args: tp.Any,
    **kwargs: tp.Any,
) -> ClientResponse:
    """Patch some fields of session."""

    method = f"tgbot/session/{id_}/"
    response = await client.patch(method, json=data, *args, **kwargs)
    return response


async def session_exists(
    chat_id: int,
    *args: tp.Any,
    **kwargs: tp.Any,
) -> bool:
    """Determine whether session for chat exists."""

    session = await fetch_session(params={"chat_id": chat_id}, *args, **kwargs)
    exists = session and session.chat_id == chat_id
    return exists


async def fetch_phone(
    chat_id: int,
    *args: tp.Any,
    **kwargs: tp.Any,
) -> str:
    """Fetch phone for **authorized** user.

    Contract: session must exist.
    """

    session = await fetch_session(params={"chat_id": chat_id}, *args, **kwargs)
    assert session is not None
    return session.phone


# ------------------------------------------------------------------------------

AuthorizeResult = namedtuple("AuthorizeResult", ["success", "details"])


async def authorize(chat_id: int, phone: str) -> AuthorizeResult:
    """Link chat with session using phone."""

    params = {"phone": phone}

    match await fetch_students(authorizing=True, params=params):
        case []:
            return AuthorizeResult(
                success=False,
                details="Студент с таким номером телефона не найден.",
            )
        case [student]:
            pass
        case _:
            return AuthorizeResult(
                success=False,
                details="Найдено несколько студентов с таким номером телефона.\n"
                        "Обратитесь к технической поддержке.",
            )

    if not student.is_milgroup_commander():
        return AuthorizeResult(
            success=False,
            details="Доступ разрешён только командирам взводов.",
        )

    session = await fetch_session(params=params)

    if student.is_milgroup_commander() and not session:
        params["chat_id"] = chat_id
        await post_session(body=params)

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
