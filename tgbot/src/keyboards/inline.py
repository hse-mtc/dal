from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from api.student import Student, State


def student_absence_keyboard(
        student_id: int,
        selected_button: int = State.present.value) -> InlineKeyboardMarkup:
    base_text = {
        State.present.value: ('Присутствует ✅', 'Отсутствует'),
        State.absent.value: ('Присутствует', 'Отсутствует ✅')
    }
    present_text, absent_text = base_text[selected_button]
    present = InlineKeyboardButton(
        present_text, callback_data=f'{State.present.value} {student_id}')
    absent = InlineKeyboardButton(
        absent_text, callback_data=f'{State.absent.value} {student_id}')

    buttons = [present, absent]

    keyboard = InlineKeyboardMarkup().row(*buttons)

    return keyboard
