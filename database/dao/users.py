from database.dao.base import BaseDao

from database.models.users import Users

from src.config import settings

from sqlalchemy import select
from datetime import date

from aiogram.exceptions import TelegramAPIError
from aiogram import Bot


class UsersDao(BaseDao):
    model = Users
    
    
    
    
    
async def run_subscription_checker(bot: Bot, async_session):
    async with async_session() as session:
        query = select(Users).where(
            Users.end_date < date.today(),
            Users.is_active == True
        )
        result = await session.execute(query)
        expired_users = result.scalars().all()
        
        for user in expired_users:
            try:
                await bot.ban_chat_member(chat_id=settings.PRIVATE_ID, user_id=user.tg_id)
                await bot.unban_chat_member(chat_id=settings.PRIVATE_ID, user_id=user.tg_id)
                
                await bot.send_message(
                    chat_id=user.tg_id,
                    text="❌ <b>Ваша подписка истекла!</b>\n\nВы были удалены из закрытого канала. Чтобы вернуть доступ, пожалуйста, продлите подписку в меню профиля."
                )
            except Exception as e:
                print(f"Ошибка при обработке пользователя {user.tg_id}: {e}")
                
                
            await UsersDao.edit_data(
                filter_by={"tg_id": user.tg_id},
                is_active=False
            )
                
    
    
    
    
    
