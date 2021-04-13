import os

DEBUG = os.environ["DEBUG"].lower() == "true"

TGBOT_PORT = int(os.environ["TGBOT_PORT"])

TIMEZONE = "Europe/Moscow"
