import os

import telebot
from telebot import apihelper

from .exception_handler import ExceptionHandler

import logging

telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


apihelper.ENABLE_MIDDLEWARE = True


TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(TOKEN, exception_handler=ExceptionHandler())
