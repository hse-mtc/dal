from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.student import State


def student_absence_keyboard(
    student_id: int,
    selected_button: int = State.PRESENT.value,
) -> InlineKeyboardMarkup:
    base_text = {
        State.PRESENT.value: ('✅ Присутствует', 'Отсутствует'),
        State.ABSENT_LA.value: ('Присутствует', '✅ Отсутствует', '☑️ Опаздывает', 'Уважительная', 'Неуважительная'),
        State.ABSENT_LE.value: ('Присутствует', '✅ Отсутствует', 'Опаздывает', '☑️ Уважительная', 'Неуважительная'),
        State.ABSENT_IL.value: ('Присутствует', '✅ Отсутствует', 'Опаздывает', 'Уважительная', '☑️ Неуважительная'),
    }
    if selected_button == State.PRESENT.value:
        present_text, absent_text = base_text[selected_button]
    else:
        present_text, absent_text, late_text, le_text, il_text = base_text[selected_button]

    present = InlineKeyboardButton(
        present_text, callback_data=f'{State.PRESENT.value} {student_id}')
    absent = InlineKeyboardButton(
        absent_text, callback_data=f'{State.ABSENT_LA.value} {student_id}')

    buttons = [[present, absent]]

    keyboard = InlineKeyboardMarkup().row(*buttons[0])

    if selected_button != State.PRESENT.value:
        late = InlineKeyboardButton(
            late_text, callback_data=f'{State.ABSENT_LA.value} {student_id}')
        le = InlineKeyboardButton(
            le_text, callback_data=f'{State.ABSENT_LE.value} {student_id}')
        il = InlineKeyboardButton(
            il_text, callback_data=f'{State.ABSENT_IL.value} {student_id}')
        buttons.append([late, le, il])

        keyboard.row(*buttons[1])

    return keyboard
