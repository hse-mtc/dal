from bot import bot
from libs import auth
from actions.greeting import send_greeting_message


@bot.message_handler(commands=['start'])
def start_command(message):
    print('/start received')

@bot.message_handler(commands=['code'])
def code_command(message):
    chat_id = message.chat.id
    if auth.check_user(chat_id):
        bot.send_message(chat_id, 'Вы уже аутентифицировались. '
                         'Если Вы хотите сбросить аутентификацию, введите команду "/reset_code"')
    elif auth.try_to_auth(chat_id, message.text.split('/code ')[1]):
        bot.send_message(chat_id, 'Вы успешно аутентифицировались!')
        send_greeting_message(chat_id)
    else:
        bot.send_message(chat_id, 'Код введен неверно. Повторите попытку ввода еще раз вызвав команду "/code КОД"')

@bot.message_handler(commands=['reset_code'])
def reset_code_command(message):
    chat_id = message.chat.id
    if auth.reset_user(chat_id):
        bot.send_message(chat_id, 'Сбор произошел успешно.')
    else:
        bot.send_message(chat_id, 'Произошла ошибка при сбросе аутентификации.')
