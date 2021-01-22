from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def base_keyboard(button_text: list[str]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for text in button_text:
        button = KeyboardButton(text)
        keyboard.add(button)
        if text == 'Главное меню':
            return keyboard

    keyboard.add('Главное меню')
    return keyboard


def start_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard(['Расход'])


def absence_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard(['Отправить данные'])


def menu_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard(['Главное меню'])
