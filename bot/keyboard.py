import calendar
from datetime import date

from aiogram.types import (CallbackQuery, KeyboardButton,
    ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.datebase.models import User
import bot.datebase.requests as rq

get_number_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поделиться контактом", request_contact=True)]],
    resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Поделиться контактом")


async def main_menu_user_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
      
    builder.add(InlineKeyboardButton(text="Записаться", callback_data="to_service"),
                InlineKeyboardButton(text="Личный кабинет", callback_data="to_account"))
    
    if is_admin:
        builder.add(InlineKeyboardButton(text="Сменить режим", callback_data="change_mode"))
        return builder.adjust(1, 2).as_markup()
    
    builder.add(InlineKeyboardButton(text="Поддержка", url="https://t.me/podolinf"))     
    return builder.adjust(1, 2).as_markup()    

async def main_menu_admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
                InlineKeyboardButton(text="Окошки", callback_data="slots"),
                InlineKeyboardButton(text="Клиенты", callback_data="clients"),
                InlineKeyboardButton(text="Сменить режим", callback_data="change_mode")
                )
    
                
    
    return builder.adjust(1, 2).as_markup()


account_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить имя", callback_data="change_name")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
])


async def calendar_keyboard(year: int, month: int, mode=False) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="<", callback_data=f"<{month}"),
        InlineKeyboardButton(text=str(calendar.month_name[month]), callback_data="_"),
        InlineKeyboardButton(text=">", callback_data=f">{month}"),
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
    slots = []
    l = 0
    for slot in (await rq.get_all_slots()):
        slots.append(slot.date)
        l += 1
    # slots = [slot.date for slot in (await rq.get_all_slots())]
    for week in a:
        for day in week:
            if day >= date.today().day or (month > date.today().month and day):
                text = str(day)
                # if f"{day}.{month}.{year}" in slots:
                #     slots.remove(f"{day}.{month}.{year}")
                #     text = text + "💅"
                for i in range(l):
                    if f"{day}.{month}.{year}" == slots[i]:
                        text = text + "💅"
                        slots.pop(i)
                        l -= 1
                        break
                builder.button(text=text, callback_data=f"!{day}.{month}.{year}")
            else:
                builder.button(text="-", callback_data="_")
    builder.button(text="Назад", callback_data="back_to_main_menu")
    return builder.adjust(3, 7).as_markup()

async def slots_keyboard(date: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    slots = await rq.get_slots(date)

    for slot in slots:
        builder.add(InlineKeyboardButton(text=f"❌{slot.time}❌", callback_data=f"/{slot.time}"))
 
    builder.add(InlineKeyboardButton(text="Назад", callback_data="back_to_add_slot"))
    return builder.adjust(1).as_markup()

