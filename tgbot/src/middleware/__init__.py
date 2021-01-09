from aiogram import Dispatcher

from .auth import AuthMiddleware


def setup(dp: Dispatcher) -> None:
    # Register `auth` middleware
    dp.middleware.setup(AuthMiddleware())
