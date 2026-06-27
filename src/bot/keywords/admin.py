from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram.filters.callback_data import CallbackData

class AdminMenuCallback(CallbackData, prefix="admin_menu"):
    action: str
    
class BackAdminCallback(CallbackData, prefix="back_admin"):
    action: str

admin_builder = InlineKeyboardBuilder()
admin_builder.button(
    text="🔄️ Обновить данные",
    callback_data=AdminMenuCallback(action="refresh_data").pack()
)
admin_builder.button(
    text="🚫 Забанить",
    callback_data=AdminMenuCallback(action="ban_user").pack()
)
admin_builder.button(
    text="➕ Продлить подписку(+30 дней)",
    callback_data=AdminMenuCallback(action="add_sub").pack()
)

back_admin_builder = InlineKeyboardBuilder()
back_admin_builder.button(
    text="🔙 Назад к меню админа",
    callback_data=BackAdminCallback(action="menu").pack()
)