from aiogram.utils.keyboard import InlineKeyboardBuilder



admin_builder = InlineKeyboardBuilder()
admin_builder.button(
    text="Статистика",
    callback_data="admin_stats"
)