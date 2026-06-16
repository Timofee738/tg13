from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

users_router = Router()

@users_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(f"Hello, welcome to this bot.\n\n")