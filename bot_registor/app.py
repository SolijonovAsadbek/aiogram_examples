import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Bot token can be obtained via https://t.me/BotFather
load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


async def main() -> None:
    from bot_registor.handler import start_router, register_router

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start_router, register_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(filename)s.%(funcName)s:%(lineno)d [%(asctime)s] :: %(levelname)s - %(message)s",
                        datefmt="%H:%M:%S",
                        stream=sys.stdout)
    asyncio.run(main())
