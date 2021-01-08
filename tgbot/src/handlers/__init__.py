from aiogram import Dispatcher

from .auth import (
    set_code,
    my_code,
    reset_code,
)


def setup(dp: Dispatcher) -> None:
    # Register `auth` handlers
    dp.register_message_handler(set_code, commands=["set_code"])
    dp.register_message_handler(my_code, commands=["my_code"])
    dp.register_message_handler(reset_code, commands=["reset_code"])

    # Register `absence` handlers
    # TODO: once they are done
