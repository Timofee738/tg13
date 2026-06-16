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
        
        if not isinstance(event, Message):
            return await handler(event, data)
        
        tg_user = event.from_user
        if not tg_user:
            return await handler(event, data)
        
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
                
                await event.answer(f"✅ You succesfully registered ✅\n\n🆔 id: {tg_user.id}\n👤 username: {tg_user.username}")
                
            data["session"] = session
            data["user"] = user
            
            return await handler(event, data)
            
        