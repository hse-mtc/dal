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


async def main() -> None:
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
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", config.TGBOT_PORT)

    # Run everything
    while True:
        try:
            await dp.skip_updates()
            await asyncio.gather(
                dp.start_polling(),
                site.start(),
            )

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
