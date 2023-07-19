import typing as tp

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from keyboards.button_texts import ButtonText


def base_keyboard(
    button_text: list[str],
    **kwargs: tp.Any,
) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    for text in button_text:
        button = KeyboardButton(text, **kwargs)
        keyboard.add(button)
        if text == ButtonText.MAIN_MENU.value:
            return keyboard

    keyboard.add(ButtonText.MAIN_MENU.value)
    return keyboard


def list_milgroup_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard([ButtonText.LIST_MILGROUP.value])


def report_absence_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard([ButtonText.REPORT_ABSENCE.value])


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard([ButtonText.MAIN_MENU.value])


def share_contact_keyboard() -> ReplyKeyboardMarkup:
    return base_keyboard(
        [ButtonText.SHARE_CONTACT.value],
        request_contact=True,
    )
