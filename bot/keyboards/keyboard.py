import calendar
from aiogram.types import (CallbackQuery, KeyboardButton,
    ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.datebase.models import User

get_number_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поделиться контактом", request_contact=True)]],
    resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Поделиться контактом")

async def main_menu_keyboard(isAdmin: bool, mode: bool) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    if isAdmin:
        if mode:
            builder.add(
                InlineKeyboardButton(text="Добавить", callback_data="add_slot"),
                InlineKeyboardButton(text="Убрать", callback_data="delete_slot"),
                )
        else:
            builder.add(InlineKeyboardButton(text="Записаться", callback_data="to_service"),
                        InlineKeyboardButton(text="Личный кабинет", callback_data="to_account"))
        
        builder.add(InlineKeyboardButton(text="Сменить режим", callback_data="change_mode"))
        return builder.adjust(1, 2).as_markup()

    else:  
        builder.add(InlineKeyboardButton(text="Записаться", callback_data="to_service"),
                    InlineKeyboardButton(text="Личный кабинет", callback_data="to_account"),
                    InlineKeyboardButton(text="Поддержка", url="https://t.me/podolinf")
        )
        return builder.adjust(1, 2).as_markup()     


#     InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="Записаться", callback_data="to_services")],
#     [InlineKeyboardButton(text="Личный кабинет", callback_data="to_account"),
#     InlineKeyboardButton(text="Поддержка", url="https://t.me/podolinf")]
# ])

account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить имя", callback_data="change_name")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
])


async def calendar_keyboard(year: int, month: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="<", callback_data=f"{month}<"),
        InlineKeyboardButton(text=str(calendar.month_name[month]), callback_data="_"),
        InlineKeyboardButton(text=">", callback_data=f"{month}>"),
    )
    builder.add(
        InlineKeyboardButton(text="Пн", callback_data="_"),
        InlineKeyboardButton(text="Вт", callback_data="_"),
        InlineKeyboardButton(text="Ср", callback_data="_"),
        InlineKeyboardButton(text="Чт", callback_data="_"),
        InlineKeyboardButton(text="Пт", callback_data="_"),
        InlineKeyboardButton(text="Сб", callback_data="_"),
        InlineKeyboardButton(text="Вс", callback_data="_")
    )
    a = calendar.monthcalendar(year, month)
    for week in a:
        for day in week:
            if day:
                builder.button(text=str(day), callback_data=" ")
            else:
                builder.button(text=" ", callback_data="_")
    builder.button(text="Назад", callback_data="back_to_main_menu")
    return builder.adjust(3, 7).as_markup()
