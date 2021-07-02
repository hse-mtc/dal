from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from api.student import State


def student_absence_keyboard(
    student_id: int,
    selected_button: int = State.PRESENT.value,
) -> InlineKeyboardMarkup:
    base_text = {
        State.PRESENT.value: ('Присутствует ✅', 'Отсутствует'),
        State.ABSENT.value: ('Присутствует', 'Отсутствует ✅')
    }
    present_text, absent_text = base_text[selected_button]
    present = InlineKeyboardButton(
        present_text, callback_data=f'{State.PRESENT.value} {student_id}')
    absent = InlineKeyboardButton(
        absent_text, callback_data=f'{State.ABSENT.value} {student_id}')

    buttons = [present, absent]

    keyboard = InlineKeyboardMarkup().row(*buttons)

    return keyboard
