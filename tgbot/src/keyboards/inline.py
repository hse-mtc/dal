from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def student_absence_keyboard(student_id: str, selected_button: str = '1') -> InlineKeyboardMarkup:
    base_text = {
        '1': ('Присутствует ✅', 'Отсутствует'),
        '0': ('Присутствует', 'Отсутствует ✅')
    }
    present_text, absent_text = base_text[selected_button]
    present = InlineKeyboardButton(present_text, callback_data=f'1 {student_id}')
    absent = InlineKeyboardButton(absent_text, callback_data=f'0 {student_id}')

    buttons = [present, absent]

    keyboard = InlineKeyboardMarkup().row(*buttons)

    return keyboard
