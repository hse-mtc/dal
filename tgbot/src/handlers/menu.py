from aiogram.types import Message

from keyboards.reply import list_milgroup_keyboard
from keyboards.button_texts import ButtonText


async def menu_handler(message: Message) -> None:
    await message.answer('Возврат в главное меню. Выберите нужное действие',
                         reply_markup=list_milgroup_keyboard())


menu_handler.handler_filters = [
    lambda message: message.text == ButtonText.MAIN_MENU.value,
]

async def start_handler(message: Message) -> None:
    if message.text == ButtonText.START.value:
        phone = await fetch_phone(chat_id=message.chat.id)
        user = await fetch_students(many=False, params={"phone": phone})
        assert isinstance(user, Student)

        await message.reply(
            textwrap.dedent(f"""
                Здравия желаю, {user.fullname.strip()}.
                
                Взвод: {user.milgroup.title}.
                Должность: {getattr(Post, user.post).value}.
                
                Нажмите кнопку "{ButtonText.LIST_MILGROUP.value}", чтобы вывести список студентов Вашего взвода.
            """),
            reply_markup=list_milgroup_keyboard(),
        )

start_handler.handler_filters = [
    lambda message: message.text == ButtonText.MAIN_MENU.value,
]
