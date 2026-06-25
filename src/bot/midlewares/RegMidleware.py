from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from database.models.users import Users

from typing import Any, Awaitable, Callable, Dict

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select

class RegMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker):
        super().__init__()
        self.session = session
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        # 1. Проверяем, что событие имеет пользователя (Message или CallbackQuery)
        if not hasattr(event, "from_user") or event.from_user is None:
            return await handler(event, data)
            
        tg_user = event.from_user
        
        # 2. Работаем с базой данных универсально для любого события
        async with self.session() as session:
            result = await session.execute(
                select(Users).where(Users.tg_id == tg_user.id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                user = Users(
                    tg_id=tg_user.id,
                    username=tg_user.username,
                    first_name=tg_user.first_name
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                
                # Отправляем приветствие только если это было текстовое сообщение
                if isinstance(event, Message):
                    await event.answer(f"✅ Вы успешно зарегистрировались ✅\n\n🆔 id: {tg_user.id}\n👤 username: {tg_user.username}")
                
            # Прокидываем данные в ЛЮБОЙ хендлер (и для сообщений, и для кнопок)
            data["session"] = session
            data["user"] = user
            
            return await handler(event, data)

            
        