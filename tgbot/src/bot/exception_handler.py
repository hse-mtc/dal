import telebot
from libs.exceptions import NotAuthorised


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        if isinstance(exception, NotAuthorised):
            return True
        return False
