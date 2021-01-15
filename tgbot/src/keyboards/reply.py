from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)


def start_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton('Расход')
    return ReplyKeyboardMarkup(resize_keyboard=True).add(button)


def absence_keyboard() -> ReplyKeyboardMarkup:
    button = KeyboardButton('Отправить данные')
    return ReplyKeyboardMarkup(resize_keyboard=True).add(button)
