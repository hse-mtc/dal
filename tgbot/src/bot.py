import asyncio
import os
import logging

from aiohttp import web

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

import handlers
import middleware

from routes import uniforms


def main() -> None:
    # Logging
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG else logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )

    # Bot
    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher(bot, storage=MemoryStorage())

    handlers.setup(dp)
    middleware.setup(dp)

    # Server
    app = web.Application()
    app.add_routes(uniforms.routes)
    app[config.BOT] = bot

    # Run everything
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(dp.skip_updates())
            loop.create_task(dp.start_polling())
            web.run_app(
                app=app,
                host="0.0.0.0",
                port=config.TGBOT_PORT,
            )
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
