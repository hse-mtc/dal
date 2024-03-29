import asyncio
import operator
from datetime import datetime

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import bold as bold_text

from api.auth import fetch_phone
from api.absence import (
    post_absence,
    fetch_today_absences,
)
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


def report_message(restriction_time):
    return bold_text(f"Время отправки ограничено до {restriction_time}.")


async def list_milgroup(message: Message, state: FSMContext) -> None:
    # TODO(TmLev): save user to local storage to prevent excessive requests.
    phone = await fetch_phone(chat_id=message.chat.id)
    user = await fetch_students(many=False, params={"phone": phone})

    if user.milgroup.weekday != datetime.now().weekday():
        await message.answer(
            bold_text("У вас нет занятий сегодня."),
            parse_mode=MD2,
            reply_markup=main_menu_keyboard(),
        )
        return

    [students, today_absences] = await asyncio.gather(
        fetch_students(params={"milgroup": user.milgroup.id}),
        fetch_today_absences(user.milgroup.id),
    )

    students.sort(key=operator.attrgetter("fullname"))
    students_by_id: dict[int, Student] = {student.id: student for student in students}

    for today_absence in today_absences:
        students_by_id[today_absence["student"]["id"]].state = State[
            today_absence["excuse"]
        ]

    await state.set_data(students_by_id)

    for student in students:
        await message.answer(
            student.fullname,
            reply_markup=student_absence_keyboard(
                student_id=student.id,
                selected_button=student.state.value,
            ),
        )

    restriction_time = await fetch_restriction_time()
    await message.answer(
        report_message(restriction_time),
        parse_mode=MD2,
        reply_markup=report_absence_keyboard(),
    )


list_milgroup.handler_filters = [
    lambda message: message.text == ButtonText.LIST_MILGROUP.value,
]


async def silent_report_absence(state: FSMContext) -> None:
    students_by_id: dict[int, Student] = await state.get_data()
    students = [student for _, student in students_by_id.items()]
    await post_absence(students)


async def toggle_student_absence_status(
    callback_query: CallbackQuery,
    state: FSMContext,
) -> None:
    if not await absence_report_overdue():
        await callback_query.answer()
        return

    if callback_query.message.date.date() != datetime.now().date():
        await callback_query.answer()
        return

    new_state, id_ = map(int, callback_query.data.split())
    students_by_id = await state.get_data()
    if new_state == students_by_id[id_].state.value:
        await callback_query.answer()
        return

    students_by_id[id_].state = State(new_state)
    await state.set_data(students_by_id)
    await silent_report_absence(state)
    await callback_query.message.edit_reply_markup(
        reply_markup=student_absence_keyboard(id_, new_state),
    )


toggle_student_absence_status.handler_filters = [
    lambda callback: True,
]


async def report_absence(message: Message, state: FSMContext) -> None:
    if not await absence_report_overdue():
        restriction_time = await fetch_restriction_time()
        await message.answer(
            report_message(restriction_time),
            parse_mode=MD2,
            reply_markup=main_menu_keyboard(),
        )
        return

    students_by_id: dict[int, Student] = await state.get_data()
    students = [student for _, student in students_by_id.items()]
    message_text = await post_absence(students)
    await message.answer(
        message_text,
        parse_mode=MD2,
        reply_markup=main_menu_keyboard(),
    )


report_absence.handler_filters = [
    lambda message: message.text == ButtonText.REPORT_ABSENCE.value,
]
