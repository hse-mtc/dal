import os

DEBUG = os.environ["DEBUG"].lower() == "true"
TOKEN = os.environ["TOKEN"]

TGBOT_PORT = int(os.environ["TGBOT_PORT"])
TGBOT_EMAIL: str = os.environ["TGBOT_EMAIL"]
TGBOT_PASSWORD = os.environ["TGBOT_PASSWORD"]

TIMEZONE = "Europe/Moscow"

BOT = "dal_tgbot"
