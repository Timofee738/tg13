from aiogram import Router, F

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.bot.keywords.admin import admin_builder

from database.dao.users import UsersDao



admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_cmd(message: Message):
    await message.answer("Hello admin 👋", reply_markup=admin_builder.as_markup())
    
    
@admin_router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    await callback.answer()
    
    today_users = await UsersDao.count_day_users()
    all_users = await UsersDao.count_users()
    
    
    text = (
        f"⚙️ <b>Панель администратора: Статистика</b>\n\n"
        f"👥 Всего пользователей в боте: <code>{all_users}</code>\n"
        f"📈 Новых за последние 24 часа: <code>{today_users}</code>\n\n"
    )
    await callback.message.edit_text(text=text,parse_mode="HTML", reply_markup=admin_builder.as_markup())
    
    
    

