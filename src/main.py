import asyncio
from aiogram import Bot, Dispatcher

from config import settings

from src.bot.handler import get_handlers_router

from database.connect import async_session


from src.bot.midlewares.RegMidleware import RegMidleware

async def main():
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(get_handlers_router())
    dp.message.outer_middleware(RegMidleware(async_session))

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__=='__main__':
    asyncio.run(main())
