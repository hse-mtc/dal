from bot import bot
from dal_api import auth
from libs.exceptions import NotAuthorised


@bot.middleware_handler(update_types=['message'])
def auth_handler(bot_instance, message, update_id=None):
    # Skip auth check for command /code
    if (text := getattr(message, 'text')) and text.split()[0] == '/code':
        return

    chat_id = message.chat.id
    if not auth.check_user(chat_id):
        bot_instance.send_message(chat_id, 'Здравия желаю, товарищ командир взвода!\n'
                         'Введите свой код с помощью команды "/code КОД"')
        # Update last_update_id to ignore this update and skip further processing this update again
        bot_instance.last_update_id = update_id
        raise NotAuthorised(f'User with chat id {chat_id} is not authorised')
