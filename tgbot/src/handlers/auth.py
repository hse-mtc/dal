import textwrap

from aiogram.types import Message

from api.student import (
    fetch_students,
    Post,
    Student,
)
from api.auth import (
    session_exists,
    authorize,
)

from keyboards.button_texts import ButtonText
from keyboards.reply import (
    list_milgroup_keyboard,
    share_contact_keyboard,
)


async def share_contact(message: Message) -> None:
    chat_id = message.chat.id
    phone = message.contact["phone_number"]
    
    if phone.startswith("+"):
        phone = phone[1:]

    if message.contact["user_id"] != chat_id:
        await message.reply(
            "Данный номер телефона принадлежит другому пользователю.",
            reply_markup=share_contact_keyboard(),
        )
        return

    if await session_exists(chat_id):
        await message.reply(
            "Вы уже авторизованы.",
            reply_markup=list_milgroup_keyboard(),
        )
        return

    result = await authorize(chat_id, phone)
    if not result.success:
        await message.reply("Не удалось авторизоваться.\n" f"{result.details}")
        return

    user = await fetch_students(many=False, params={"phone": phone})
    assert isinstance(user, Student)

    await message.reply(
        textwrap.dedent(f"""
            Здравия желаю, {user.fullname.strip()}.
            
            Взвод: {user.milgroup.title}.
            Должность: {getattr(Post, user.post).value}.
            
            Нажмите кнопку "{ButtonText.LIST_MILGROUP.value}", чтобы вывести список студентов Вашего взвода.
        """),
        reply_markup=list_milgroup_keyboard(),
    )
