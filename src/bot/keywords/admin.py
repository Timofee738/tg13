from aiogram.utils.keyboard import InlineKeyboardBuilder



admin_builder = InlineKeyboardBuilder()
admin_builder.button(
    text="🔄️ Обновить данные",
    callback_data="admin"
)