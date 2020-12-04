from bot import bot


if __name__ == '__main__':
    print('Telegram Bot is now running')
    bot.polling(none_stop=True)
