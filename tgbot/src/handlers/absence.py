import typing as tp

from collections import namedtuple

from asyncio import gather

from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import CallbackQuery

from api.auth import (
    session_exists,
    fetch_user
)

from api.student import fetch_students

from keyboards.inline import student_absence_keyboard
from keyboards.reply import absence_keyboard

MD2 = ParseMode.MARKDOWN_V2


async def get_student(message: Message) -> None:
    chat_id = message.chat.id
    user = await fetch_user(chat_id)
    kek = []
    global students
    students = await fetch_students(user.milgroup)
    # TODO: combine all answers and wait for them
    for student in students:
        kek.append(
            message.answer(
            student.full_name,
            reply_markup=student_absence_keyboard(student.id, )
        ))
    await gather(*kek)
    await message.answer('После того, как отметите всех студентов, нажмите\n'
                         'кнопку "Отправить"',
                         reply_markup=absence_keyboard())
    return


async def callback_query_process(callback_query: CallbackQuery) -> None:
    data = callback_query.data
    state, student_id = data.split()
    for student in students:
        if student.id == student_id:
            student.state = state

async def absence_sending(message: Message) -> None:
    print(students)
