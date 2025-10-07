import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers.user import router as user_router
from bot.handlers.admin import router as admin_router
from bot.datebase.models import async_main

from settings import settings


async def main():
    await async_main()

    
    bot_token = settings.BOT_TOKEN
    
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(user_router, admin_router)
    

    await dp.start_polling(bot)

 


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")