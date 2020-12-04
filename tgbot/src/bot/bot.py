import os
import logging

import telebot
from telebot import apihelper

from .exception_handler import ExceptionHandler


class TeleBot(telebot.TeleBot):
    """
    Override default TeleBot to pass update_id to middleware
    """
    def process_middlewares(self, update):
        for update_type, middlewares in self.typed_middleware_handlers.items():
            if getattr(update, update_type) is not None:
                for typed_middleware_handler in middlewares:
                    # Pass update_id here ---------------------------------------v
                    typed_middleware_handler(self, getattr(update, update_type), update_id=update.update_id)

        if len(self.default_middleware_handlers) > 0:
            for default_middleware_handler in self.default_middleware_handlers:
                default_middleware_handler(self, update)


telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
apihelper.ENABLE_MIDDLEWARE = True

TOKEN = os.environ.get('TOKEN')

bot = TeleBot(TOKEN, exception_handler=ExceptionHandler())
