from aiogram.types import Message

from keyboards.reply import start_keyboard


async def menu_handler(message: Message) -> None:
    await message.answer(
        'Возврат в главное меню. Выберите нужное действие',
        reply_markup=start_keyboard())
