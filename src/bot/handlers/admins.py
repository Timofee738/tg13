from aiogram import Router, F

from aiogram.filters import Command
from aiogram.types import Message

from src.bot.keywords.admin import admin_builder

from database.dao.users import UsersDao

from sqlalchemy import select, func

from database.models.users import Users
from database.models.payments import Payments
from database.connect import async_session

from datetime import timedelta, datetime, timezone, date



admin_router = Router()
    
    
@admin_router.message(Command("admin"))
async def admin_stats(message: Message):
    async with async_session() as session:
        query1 = select(func.count(Users.tg_id))
        result1 = await session.execute(query1)
        all_users = result1.scalar() or 0
        
        day = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=1)
        query2 = select(func.count(Users.tg_id)).where(Users.created_at >= day)
        result2 = await session.execute(query2)
        today_users = result2.scalar() or 0
        
        day_now = date.today()
        query3 = select(func.count(Users.tg_id)).where(Users.end_date >= day_now)
        result3 = await session.execute(query3)
        subs = result3.scalar() or 0
        
        query4 = select(func.sum(Payments.amount))
        result4 = await session.execute(query4)
        total_earnings = result4.scalar() or 0
        
    
    text = (
        f"⚙️ <b>Панель администратора: Статистика</b>\n\n"
        f"👥 Всего пользователей в боте: <code>{all_users}</code>\n"
        f"📈 Новых за последние 24 часа: <code>{today_users}</code>\n"
        f"✨ Общее количество активных подписок: <code>{subs}</code>\n\n"
        f"💰 Заработано за всё время: <code>{total_earnings:,.2f} руб.</code>\n"
    )
    await message.answer(text=text,parse_mode="HTML", reply_markup=admin_builder.as_markup())
    
    
    

