from bot import bot
from dal_api import auth


@bot.message_handler(commands=['code'])
def code_command(message):
    chat_id = message.chat.id
    code = message.text.split('/code')[1].strip()

    if auth.check_user(chat_id):
        reply = 'Вы уже аутентифицировались. Если Вы хотите сбросить аутентификацию, введите команду "/reset_code"'
    elif auth.try_to_auth(chat_id, code):
        reply = 'Здравия желаю, {}, товарищ командир взвода {}!'.format(
                                auth.get_user_name(chat_id),
                                auth.get_user_milgroup(chat_id)
                            )
    else:
        reply = 'Код введен неверно. Повторите попытку ввода еще раз вызвав команду "/code <КОД>"'
    bot.send_message(chat_id, reply)

@bot.message_handler(commands=['reset_code'])
def reset_code_command(message):
    chat_id = message.chat.id
    if auth.reset_user(chat_id):
        reply = 'Сбор произошел успешно.'
    else:
        reply = 'Произошла ошибка при сбросе аутентификации.'
    bot.send_message(chat_id, reply)
