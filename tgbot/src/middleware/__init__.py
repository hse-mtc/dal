from aiogram import Dispatcher

from .auth import AuthMiddleware


def setup(dp: Dispatcher) -> None:
    # Register `logging` middleware
    # TODO

    # Register `auth` middleware
    dp.middleware.setup(AuthMiddleware())
