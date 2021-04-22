import operator

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import bold as bold_text

from api.auth import (session_exists, fetch_user, fetch_phone)

from api.student import fetch_students, State
from api.absence import post_absence

from keyboards.inline import student_absence_keyboard
from keyboards.reply import absence_keyboard, menu_keyboard

from utils.time import absence_report_overdue, fetch_restriction_time

MD2 = ParseMode.MARKDOWN_V2


async def get_student(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    phone = await fetch_phone(chat_id)

    user = await fetch_user(phone)

    students = await fetch_students(user.milgroup)
    await state.set_data(students)

    # TODO: now we have no idea how to sort list with Student objects
    # inside `gather`. We need to collect `message.anwser` tasks and pull
    # it into `gather`. But it have to be sorted.
    # This is not final realisation.
    for student in sorted(students, key=operator.attrgetter('full_name')):
        await message.answer(student.full_name,
                             reply_markup=student_absence_keyboard(student.id))

    restriction_time = await fetch_restriction_time()
    await message.answer(
        f'После того, как отметите всех студентов, нажмите '
        f'кнопку "Отправить данные"\n\n'
        f'{bold_text(f"Время отправки ограничено до {restriction_time}!")}',
        parse_mode=MD2,
        reply_markup=absence_keyboard()
    )


async def callback_query_process(callback_query: CallbackQuery,
                                 state: FSMContext) -> None:
    data = callback_query.data
    message = callback_query.message

    student_state, student_id = map(int, data.split())

    students = await state.get_data()
    for student in students:
        if student_id == student.id:
            student.state = State(student_state)

    await state.set_data(students)

    await message.edit_reply_markup(
        reply_markup=student_absence_keyboard(student_id, student_state))


async def send_absence(message: Message, state: FSMContext) -> None:
    if not await absence_report_overdue():
        restriction_time = await fetch_restriction_time()
        await message.answer(
            f'Товарищ командир взвода, время отправки ограничено ' \
            f'до {restriction_time}!',
            reply_markup=menu_keyboard()
        )
        return
    students = await state.get_data()
    message_text = await post_absence(students)
    await message.answer(message_text, reply_markup=menu_keyboard())
