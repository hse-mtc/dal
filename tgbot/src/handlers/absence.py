import operator

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import bold as bold_text

from api.auth import fetch_phone
from api.absence import post_absence
from api.student import (
    fetch_students,
    State,
    Student,
)

from keyboards.inline import student_absence_keyboard
from keyboards.button_texts import ButtonText
from keyboards.reply import (
    report_absence_keyboard,
    main_menu_keyboard,
)

from utils.time import absence_report_overdue, fetch_restriction_time

MD2 = ParseMode.MARKDOWN_V2


async def list_milgroup(message: Message, state: FSMContext) -> None:
    # TODO(TmLev): save user to local storage to prevent excessive requests.
    phone = await fetch_phone(chat_id=message.chat.id)
    user = await fetch_students(many=False, params={"phone": phone})

    students = await fetch_students(params={"milgroup": user.milgroup.id})
    students.sort(key=operator.attrgetter("fullname"))

    students_by_id = {student.id: student for student in students}
    await state.set_data(students_by_id)

    for student in students:
        await message.answer(
            student.fullname,
            reply_markup=student_absence_keyboard(student.id),
        )

    restriction_time = await fetch_restriction_time()
    await message.answer(
        bold_text(f"Время отправки ограничено до {restriction_time}."),
        parse_mode=MD2,
        reply_markup=report_absence_keyboard(),
    )


list_milgroup.handler_filters = [
    lambda message: message.text == ButtonText.LIST_MILGROUP.value,
]


async def toggle_student_absence_status(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    new_state, id_ = map(int, callback_query.data.split())
    students_by_id = await state.get_data()
    students_by_id[id_].state = State(new_state)
    await state.set_data(students_by_id)
    await callback_query.message.edit_reply_markup(
        reply_markup=student_absence_keyboard(id_, new_state),)


toggle_student_absence_status.handler_filters = [
    lambda callback: True,
]


async def report_absence(message: Message, state: FSMContext) -> None:
    if not await absence_report_overdue():
        restriction_time = await fetch_restriction_time()
        await message.answer(
            f"Время отправки ограничено до {restriction_time}.",
            reply_markup=main_menu_keyboard(),
        )
        return

    students_by_id: dict[int, Student] = await state.get_data()
    students = [student for _, student in students_by_id.items()]
    message_text = await post_absence(students)
    await message.answer(message_text, reply_markup=main_menu_keyboard())


report_absence.handler_filters = [
    lambda message: message.text == ButtonText.REPORT_ABSENCE.value,
]
