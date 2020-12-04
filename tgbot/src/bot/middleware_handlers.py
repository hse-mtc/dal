from bot import bot
from libs import auth
from libs.exceptions import NotAuthorised


@bot.middleware_handler(update_types=['message'])
def auth_handler(bot_instance, message):
    chat_id = message.chat.id
    if auth.check_user(chat_id):
        bot_instance.send_message(chat_id, 'Здравия желаю, товарищ командир взвода!\n'
                         'Введите свой код с помощью команды "/code КОД"')
        raise NotAuthorised(f'User with chat id {chat_id} is not authorised')
