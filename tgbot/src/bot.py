import os

import telebot


TOKEN = os.environ.get('TOKEN')

bot = telebot.Telebot(TOKEN)
