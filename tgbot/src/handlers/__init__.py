from aiogram import Dispatcher
from aiogram.types.message import ContentType

from .auth import (
    share_contact,
    my_code,
    reset_code,
)

from .absence import (
    get_student,
    callback_query_process,
    send_absence,
)

from .menu import menu_handler


def setup(dp: Dispatcher) -> None:
    # Register `auth` handlers
    dp.register_message_handler(my_code, commands=["my_code"])
    dp.register_message_handler(reset_code, commands=["reset_code"])

    dp.register_message_handler(
        share_contact,
        content_types=ContentType.CONTACT
    )
    # Register `absence` handlers
    dp.register_message_handler(
        menu_handler,
        lambda message: message.text and message.text == 'Главное меню',
    )
    dp.register_message_handler(
        get_student,
        lambda message: message.text and message.text == 'Расход',
        state='*',
    )
    dp.register_callback_query_handler(
        callback_query_process,
        lambda callback: True,
        state='*',
    )
    dp.register_message_handler(
        send_absence,
        lambda message: message.text and message.text == 'Отправить данные',
        state='*',
    )
