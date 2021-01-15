from aiogram import Dispatcher

from .auth import (
    set_code,
    my_code,
    reset_code,
)

from .absence import (
    get_student,
    callback_query_process,
    absence_sending
)


def setup(dp: Dispatcher) -> None:
    # Register `auth` handlers
    dp.register_message_handler(set_code, commands=["set_code"])
    dp.register_message_handler(my_code, commands=["my_code"])
    dp.register_message_handler(reset_code, commands=["reset_code"])
    dp.register_message_handler(get_student, lambda message: message.text and message.text == 'Расход')
    dp.register_callback_query_handler(callback_query_process, lambda callback: True)
    dp.register_message_handler(absence_sending, lambda message: message.text and message.text == 'Отправить данные')

    # Register `absence` handlers
    # TODO: once they are done
