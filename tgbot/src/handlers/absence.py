import typing as tp

from collections import namedtuple

from asyncio import gather

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from api.auth import (
    session_exists,
    fetch_user
)

from api.student import fetch_students
from api.absence import post_all_absence

from keyboards.inline import student_absence_keyboard
from keyboards.reply import absence_keyboard

MD2 = ParseMode.MARKDOWN_V2


async def get_student(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id

    user = await fetch_user(chat_id)
    message_tasks = []

    students = await fetch_students(user.milgroup)
    await state.set_data(students)

    for student in students:
        message_tasks.append(
            message.answer(
            student.full_name,
            reply_markup=student_absence_keyboard(student.id)
        ))
    await gather(*message_tasks)

    await message.answer('После того, как отметите всех студентов, нажмите\n'
                         'кнопку "Отправить данные"',
                         reply_markup=absence_keyboard())
    return


async def callback_query_process(
    callback_query: CallbackQuery,
    state: FSMContext
) -> None:
    data = callback_query.data
    message = callback_query.message
    
    selected_button, student_id = data.split()

    students = await state.get_data()
    for student in students:
        if int(student_id) == student.id:
            student.state = int(selected_button)

    await state.set_data(students)

    await message.edit_reply_markup(
        reply_markup=student_absence_keyboard(
            student_id,
            selected_button
        )
    )


async def send_abcense(message: Message, state: FSMContext) -> None:
    students = await state.get_data()
    message_text = await post_all_absence(students)
    await message.answer(message_text)
    return
