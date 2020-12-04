from bot import bot
from libs import auth

def send_greeting_message(chat_id):
    bot.send_message(chat_id, 'Здравия желаю, {}, '
                        'товарищ командир взвода {}!'.format(
                            auth.get_user_name(chat_id),
                            auth.get_user_milgroup(chat_id)
                        ))
