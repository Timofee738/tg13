from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Any, Awaitable, Callable, Dict
from src.config import settings

class AdminMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: set[int]):
        super().__init__()
        self.admin_ids = admin_ids
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        user = getattr(event, "from_user", None)
        
        if user:
            if user.id not in self.admin_ids and user.id not in settings.ADMINS:
                
                if isinstance(event, CallbackQuery):
                    await event.answer()
                    return
                

                if isinstance(event, Message):
                    return
                
                return  

        return await handler(event, data)