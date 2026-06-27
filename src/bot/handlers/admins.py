from aiogram import Router, F

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.bot.keywords.admin import admin_builder, AdminMenuCallback, BackAdminCallback, back_admin_builder

from database.dao.users import UsersDao

from sqlalchemy import select, func

from database.models.users import Users
from database.models.payments import Payments
from database.connect import async_session

from datetime import timedelta, datetime, timezone, date

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


admin_router = Router()



class AdminBanUser(StatesGroup):
    username = State()
    
    
@admin_router.message(Command("admin"))
@admin_router.callback_query(AdminMenuCallback.filter(F.action=="refresh_data"))
@admin_router.callback_query(BackAdminCallback.filter(F.action=="menu"))
async def admin_stats(event: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    
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
        raw_earnings = result4.scalar()
        total_earnings = float(raw_earnings) if raw_earnings is not None else 0.0
        
    
    text = (
        f"⚙️ <b>Панель администратора: Статистика</b>\n\n"
        f"👥 Всего пользователей в боте: <code>{all_users}</code>\n"
        f"📈 Новых за последние 24 часа: <code>{today_users}</code>\n"
        f"✨ Общее количество активных подписок: <code>{subs}</code>\n\n"
        f"💰 Заработано за всё время: <code>{total_earnings:,.2f} руб.</code>\n"
    )
    
    if isinstance(event, Message):
        
            await event.answer(
                text=text,
                parse_mode="HTML", 
                reply_markup=admin_builder.as_markup()
            )
    elif isinstance(event, CallbackQuery):
        try:
            await event.message.answer(
                text=text,
                parse_mode="HTML", 
                reply_markup=admin_builder.as_markup()
            )
        except Exception:
            pass
        
        await event.answer("🔄 Данные успешно обновлены!")
    
    
    
    
    
    
@admin_router.callback_query(AdminMenuCallback.filter(F.action=="ban_user"))
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Напишите username пользователя которого хотите забанить: ",
        reply_markup=back_admin_builder.as_markup()
    )
    
    await state.set_state(AdminBanUser.username)
    


@admin_router.message(AdminBanUser.username)
async def capture_username_or_id(message: Message, state: FSMContext):
    input_data = message.text.strip()
    user = None
    search_criteria = ""

    if input_data.isdigit():
        target_id = int(input_data)
        search_criteria = f"с ID <code>{target_id}</code>"
        user = await UsersDao.edit_data(filter_by={"tg_id": target_id}, is_active=False)
    else:
        clean_username = input_data.replace("@", "")
        search_criteria = f"с юзернеймом @{clean_username}"
        user = await UsersDao.edit_data(filter_by={"username": clean_username}, is_active=False)

    if user:
        text = (
            f"🚫 <b>Пользователь успешно заблокирован</b>\n\n"
            f"👤 <b>Пользователь:</b> @{user.username or 'Скрыт'}\n"
            f"🆔 <b>ID:</b> <code>{user.tg_id}</code>\n"
            f"⚙️ <i>Доступ к функциям бота для него полностью ограничен.</i>"
        )
        await message.answer(text=text, parse_mode="HTML", reply_markup=back_admin_builder.as_markup())
    else:
        text = (
            f"⚠️ <b>Пользователь не найден</b>\n\n"
            f"Пользователь {search_criteria} отсутствует в базе данных бота.\n\n"
            f"📌 <b>Возможные причины:</b>\n"
            f"• Он ещё ни разу не запускал этого бота.\n"
            f"• Данные указаны с ошибкой (проверьте цифры/буквы).\n"
            f"• Пользователь недавно изменил свой @username.\n\n"
            f"💡 <i>Вы можете попробовать ввести данные повторно или вернуться в меню.</i>"
        )
        await message.answer(text=text, parse_mode="HTML", reply_markup=back_admin_builder.as_markup())
        
    await state.clear()



class AddSubState(StatesGroup):
    username = State()
    

@admin_router.callback_query(AdminMenuCallback.filter(F.action == "add_sub"))
async def add_sub(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await callback.message.edit_text(
        text="Напишите юзернейм или ID юзера, которому хотите добавить подписку:",
        reply_markup=back_admin_builder.as_markup()
    )
    await state.set_state(AddSubState.username) 


@admin_router.message(AddSubState.username)
async def capture_username_id(message: Message, state: FSMContext):
    input_data = message.text.strip()
    target_user = None
    search_criteria = ""
    
    if input_data.isdigit():
        target_id = int(input_data)
        search_criteria = f"с ID <code>{target_id}</code>"
        target_user = await UsersDao.find_one_or_none(tg_id=target_id)
    else:
        clean_username = input_data.replace("@", "")
        search_criteria = f"с юзернеймом @{clean_username}"
        target_user = await UsersDao.find_one_or_none(username=clean_username)

    if not target_user:
        text = (
            f"⚠️ <b>Пользователь не найден</b>\n\n"
            f"Пользователь {search_criteria} отсутствует в базе данных бота.\n\n"
            f"📌 <b>Возможные причины:</b>\n"
            f"• Он ещё ни разу не запускал этого бота.\n"
            f"• Данные указаны с ошибкой (проверьте цифры/буквы).\n"
            f"• Пользователь недавно изменил свой @username.\n\n"
            f"💡 <i>Вы можете попробовать ввести данные повторно или вернуться в меню.</i>"
        )
        await message.answer(text=text, parse_mode="HTML", reply_markup=back_admin_builder.as_markup())
        await state.clear()
        return

    current_date = target_user.end_date if (target_user.end_date and target_user.end_date >= date.today()) else date.today()
    new_date = current_date + timedelta(days=30)

    updated_user = await UsersDao.edit_data(
        filter_by={"tg_id": target_user.tg_id}, 
        end_date=new_date
    )

    if updated_user:
        text = (
            f"✨ <b>Пользователю успешно начислено 30 дней подписки</b>\n\n"
            f"👤 <b>Пользователь:</b> @{updated_user.username or 'Скрыт'}\n"
            f"🆔 <b>ID:</b> <code>{updated_user.tg_id}</code>\n"
            f"📅 <b>Новый срок действия:</b> <code>{updated_user.end_date}</code>"
        )  
        await message.answer(text=text, parse_mode="HTML", reply_markup=back_admin_builder.as_markup())
        
    await state.clear()
    
    
    

