import asyncio
from aiogram import Bot, Dispatcher

from config import settings

from src.bot.handler import get_handlers_router

from database.connect import async_session
from database.dao.users import run_subscription_checker


from src.bot.midlewares.RegMidleware import RegMiddleware
from src.bot.midlewares.ban import BanMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def main():
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(await get_handlers_router())
    
    dp.message.outer_middleware(RegMiddleware(session=async_session))
    dp.callback_query.outer_middleware(RegMiddleware(session=async_session))
    dp.message.outer_middleware(BanMiddleware())
    dp.callback_query.outer_middleware(BanMiddleware())
    
    scheduler = AsyncIOScheduler()
    
    scheduler.add_job(
        run_subscription_checker, 
        trigger="cron", 
        hour=0, 
        minute=0, 
        args=[bot, async_session]
    )
    
    scheduler.start()
    

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__=='__main__':
    asyncio.run(main())
