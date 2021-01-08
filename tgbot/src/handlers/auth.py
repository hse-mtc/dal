import typing as tp

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.utils.markdown import code as md_code

from api.auth import (
    session_exists,
    fetch_code,
    authorize,
    deauthorize,
    fetch_user,
)

MD2 = ParseMode.MARKDOWN_V2


async def set_code(message: Message) -> None:
    chat_id = message.chat.id
    if await session_exists(chat_id):
        await message.reply("Вы уже авторизованы.\n"
                            "Для сброса введите команду /reset_code")
        return

    code = message.text.removeprefix("/set_code").strip()
    if not code:
        await message.reply("Код пуст, попробуйте ещё раз")
        return

    result = await authorize(chat_id, code)
    if not result.success:
        await message.reply("Не удалось авторизоваться.\n" f"{result.details}")
        return

    user = await fetch_user(chat_id)
    await message.reply(f"Здравия желаю, {user.full_name}!\n"
                        f"Должность: командир взвода {user.platoon}")


async def my_code(message: Message) -> None:
    # `fetch_code` contract is fulfilled by auth middleware
    code = await fetch_code(message.chat.id)
    await message.reply(f"Текущий код: {md_code(code)}", parse_mode=MD2)


async def reset_code(message: Message) -> None:
    chat_id = message.chat.id
    result = await deauthorize(chat_id)

    if result.success:
        await message.reply("Код успешно сброшен")
    else:
        await message.reply("Не удалось сбросить код.\n" f"{result.details}")
