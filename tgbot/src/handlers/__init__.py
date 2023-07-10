from aiogram import Dispatcher
from aiogram.types.message import ContentType

from .menu import menu_handler, start_handler

from .auth import share_contact

from .absence import (
    list_milgroup,
    toggle_student_absence_status,
    report_absence,
)


def setup(dp: Dispatcher) -> None:
    # Register `menu`.
    dp.register_message_handler(
        menu_handler,
        *menu_handler.handler_filters,
    )

    # Register `/start`.
    dp.register_message_handler(
        start_handler,
        *start_handler.handler_filters,
    )

    # Register `auth` handlers.
    dp.register_message_handler(
        share_contact,
        content_types=ContentType.CONTACT,
    )

    # Register `absence` handlers.
    dp.register_message_handler(
        list_milgroup,
        *list_milgroup.handler_filters,
        state='*',
    )
    dp.register_callback_query_handler(
        toggle_student_absence_status,
        *toggle_student_absence_status.handler_filters,
        state='*',
    )
    dp.register_message_handler(
        report_absence,
        *report_absence.handler_filters,
        state='*',
    )
