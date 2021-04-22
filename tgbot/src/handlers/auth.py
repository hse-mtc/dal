from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.utils.markdown import code as md_code

from api.auth import (
    session_exists,
    fetch_phone,
    authorize,
    deauthorize,
    fetch_user,
)

from keyboards.reply import start_keyboard, share_contact_keyboard

MD2 = ParseMode.MARKDOWN_V2


async def share_contact(message: Message) -> None:
    chat_id = message.chat.id
    phone = message.contact["phone_number"]

    if message.contact["user_id"] != chat_id:
        await message.reply(
            "Поделитесь Вашим контактом, нажав на кнопку!",
            reply_markup=share_contact_keyboard()
        )

    if await session_exists(chat_id):
        await message.reply("Вы уже авторизованы!", reply_markup=start_keyboard())
        return

    result = await authorize(chat_id, phone)
    if not result.success:
        await message.reply("Не удалось авторизоваться.\n" f"{result.details}")
        return

    user = await fetch_user(phone)
    await message.reply(
        f"Здравия желаю, {user.full_name}!\n"
        f"Должность: командир взвода {user.milgroup}\n"
        "Нажмите кнопку \"Расход\", чтобы начать отмечать студентов!",
        reply_markup=start_keyboard())


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
