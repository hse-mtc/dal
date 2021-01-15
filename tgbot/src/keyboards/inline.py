from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def student_absence_keyboard(student_id: str) -> InlineKeyboardMarkup:
    present = InlineKeyboardButton('Присутствует', callback_data=f'0 {student_id}')
    absent = InlineKeyboardButton('Отсутствует', callback_data=f'1 {student_id}')

    buttons = [present, absent]

    keyboard = InlineKeyboardMarkup().row(*buttons)

    return keyboard
