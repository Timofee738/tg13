from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

main_builder = InlineKeyboardBuilder()
main_builder.button(
    text="💰 Купить подписку",
    callback_data="buy_sub"
)
main_builder.button(
    text="ℹ️ О клубе",
    callback_data="club_info"
)
main_builder.button(
    text="👤 Мой профиль",
    callback_data="profile"
)
main_builder.adjust(2, 1)


sub_builder = InlineKeyboardBuilder()
sub_builder.button(
    text="1 месяц — 990 руб",
    callback_data="1st_sub"
)
sub_builder.button(
    text="3 месяца — 2490 руб",
    callback_data="2d_sub"
)
sub_builder.button(
    text="🔙 Назад к меню",
    callback_data="menu"
)
sub_builder.adjust(1)


back_builder = InlineKeyboardBuilder()
back_builder.button(
    text="🔙 Назад к меню",
    callback_data="menu"
)


