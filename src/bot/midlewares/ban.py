from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class BanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        user = data.get("user")
        
        if not user:
            return await handler(event, data)
        
        if not user.is_active:
            if isinstance(event, Message):
                await event.answer("🚫 <b>Доступ ограничен</b>\n\nВаш аккаунт заблокирован администрацией бота.", parse_mode="HTML")
                
            elif isinstance(event, CallbackQuery):
                await event.answer("🚫 Вы заблокированы!", show_alert=True)
            return
        
        return await handler(event, data)  
            
        