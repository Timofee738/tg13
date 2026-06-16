from aiogram import Router

from aiogram.filters import Command
from aiogram.types import Message



admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_cmd(message: Message):
    await message.answer("Hello admin 👋")

