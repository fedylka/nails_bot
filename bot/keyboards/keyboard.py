from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
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
                InlineKeyboardButton(text="Добавить окошки", callback_data="add_slot"),
                InlineKeyboardButton(text="Убрать окошки", callback_data="delete_slot"))
        else:
            builder.add(InlineKeyboardButton(text="Записаться", callback_data="to_service"))
        
        builder.add(InlineKeyboardButton(text="Сменить режим", callback_data="change_mode"))
        return builder.adjust(2).as_markup()

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

