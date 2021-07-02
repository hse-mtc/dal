from aiogram.types import Message

from keyboards.reply import list_milgroup_keyboard
from keyboards.button_texts import ButtonText


async def menu_handler(message: Message) -> None:
    await message.answer('Возврат в главное меню. Выберите нужное действие',
                         reply_markup=list_milgroup_keyboard())


menu_handler.handler_filters = [
    lambda message: message.text == ButtonText.MAIN_MENU.value,
]
