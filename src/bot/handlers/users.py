from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from datetime import date

from src.config import settings

from database.models.users import Users
from database.dao.users import UsersDao

from src.bot.keywords.users import main_builder, sub_builder, back_builder

users_router = Router()

@users_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        text="Приветствуем в <b>?</b>! 👋 Здесь вы можете купить подписку на закрытый тг-канал от <b>?</b>.",
        parse_mode="HTML",
        reply_markup=main_builder.as_markup()
    )
    
@users_router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Приветствуем в <b>?</b>! 👋 Здесь вы можете купить подписку на закрытый тг-канал от <b>?</b>.",
        parse_mode="HTML",
        reply_markup=main_builder.as_markup()
    )
    
    
@users_router.callback_query(F.data == "club_info")
async def club_info(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="About info......",
        reply_markup=back_builder.as_markup()
    )
    
    
    
@users_router.callback_query(F.data == "buy_sub")
async def choose_sub(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        text="Выберете тариф:",
        reply_markup=sub_builder.as_markup()
    )
    
@users_router.callback_query(F.data == "profile")
async def proile(callback: CallbackQuery, user: Users):
    await callback.answer()
    
    name_updated_text = ""
    current_first_name = callback.from_user.first_name
    
    
    if user.first_name != current_first_name:
        await UsersDao.edit_data(
            filter_by={"tg_id": user.tg_id},
            first_name=current_first_name
        )
        user.first_name=current_first_name
        name_updated_text = "\n\n<i>(Ваше имя в базе данных было автоматически обновлено!)</i>"
        
        
    text = (
        f"👤 <b>Твой профиль:</b>\n"
        f"• Имя: {user.first_name}\n"
        f"• Username: @{user.username if user.username else 'нет'}\n"
        f"• Telegram ID: <code>{user.tg_id}</code>\n"
        f"• Подписка активна до: <code>{user.end_date if user.end_date else 'Нет подписки'}</code>"
        f"{name_updated_text}\n\n"
    )
    
    
    
    if not user.end_date or user.end_date < date.today():
        text += "❌ У вас нет активной подписки! Пожалуйста, оплатите её в профиле."
        await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=back_builder.as_markup())
        return
    
    
    try:
        invite_link = await callback.bot.create_chat_invite_link(
            chat_id=settings.PRIVATE_ID,
            member_limit=1,
            name=f"User {user.tg_id} (@{user.username if user.username else 'no_user'})"
        )
        
        text += (
            f"🎁 Ваша уникальная одноразовая ссылка для входа в канал:\n\n"
            f"{invite_link.invite_link}\n\n"
            f"⚠️ Внимание: ссылка сработает только 1 раз для 1 аккаунта!"
        )
    except Exception as e:
        text += "⚠️ Произошла ошибка при создании ссылки. Обратитесь к администратору."
        print(f"Ошибка создания ссылки: {e}")
        
        
    await callback.message.edit_text(text=text, parse_mode="HTML", reply_markup=back_builder.as_markup())

    
    


    
    
    
