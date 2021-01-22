import os
import logging

from aiogram import (
    Bot,
    Dispatcher,
    executor,
)

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import handlers
import middleware


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )

    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher(bot, storage=MemoryStorage())

    handlers.setup(dp)
    middleware.setup(dp)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
