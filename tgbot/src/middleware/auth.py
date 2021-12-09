from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message

from api.auth import session_exists

from keyboards.reply import share_contact_keyboard


class AuthMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()

    async def on_pre_process_message(self, message: Message, _: dict) -> None:
        # User is trying to authorize.
        if message.contact:
            return

        # User is already authorized.
        if await session_exists(chat_id=message.chat.id):
            return

        # User is not authorized and is not trying to authorize, cancel handler.
        await message.reply(
            "Для работы с ботом необходимо авторизоваться – "
            "поделитесь контактом, чтобы продолжить.",
            reply_markup=share_contact_keyboard(),
        )

        raise CancelHandler()
