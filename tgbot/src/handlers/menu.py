from aiogram.types import Message

from messages.message_texts import get_hello_message
from keyboards.reply import list_milgroup_keyboard
from keyboards.button_texts import ButtonText

from api.auth import fetch_phone
from api.student import (
    fetch_students,
    Post,
    Student,
)


async def menu_handler(message: Message) -> None:
    await message.answer(
        "Возврат в главное меню. Выберите нужное действие",
        reply_markup=list_milgroup_keyboard(),
    )


menu_handler.handler_filters = [
    lambda message: message.text == ButtonText.MAIN_MENU.value,
]


async def start_handler(message: Message) -> None:
    phone = await fetch_phone(chat_id=message.chat.id)
    user = await fetch_students(many=False, params={"phone": phone})
    assert isinstance(user, Student)

    await message.reply(
        get_hello_message(
            user.fullname.strip(),
            user.milgroup.title,
            getattr(Post, user.post).value,
        ),
        reply_markup=list_milgroup_keyboard(),
    )
