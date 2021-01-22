from aiogram.types import Message

from keyboards.reply import menu_keyboard, start_keyboard


async def menu_handler(message: Message) -> None:
    await message.answer('Какой-то текст', reply_markup=start_keyboard())
