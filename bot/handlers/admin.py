from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter, Command
from aiogram.exceptions import TelegramBadRequest

from re import fullmatch

import bot.keyboard as kb
import bot.datebase.requests as rq
import bot.states as st
from bot.handlers.user import delete_last_keyboard

from bot.settings import settings


router = Router()


@router.message(st.AdminMenuStates.day_slot)
@router.callback_query(F.data == "slots", st.UserMenuStates.main_menu)
async def process_day_slot(event: Message|CallbackQuery, state: FSMContext) -> None:
    text = "Выбери нужные даты:"
    if isinstance(event, Message):
        await delete_last_keyboard(event, state)
        last_msg = await event.answer(
            text=text,
            reply_markup=await kb.calendar_keyboard(event.date.year, event.date.month, True)
        )
        await state.update_data(last_message_id=last_msg.message_id)
    else:
        await state.set_state(st.AdminMenuStates.day_slot)
        await event.answer()
        await event.message.edit_text(
            text=text,
            reply_markup=await kb.calendar_keyboard(event.message.date.year, event.message.date.month, True)
        )



@router.callback_query(F.data == "_")
async def quick_callback(callback: CallbackQuery) -> None:
    await callback.answer()


@router.callback_query(F.data[0] == ">")
async def next_moth(callback: CallbackQuery) -> None:
    if int(callback.data[1:]) > callback.message.date.month:
        await callback.answer("Превышен лимит")
    else:
        await callback.answer()
        year = callback.message.date.year
        month = int(callback.data[1:]) + 1
        if month > 12:
            year += 1
            month = 1
        await callback.message.edit_reply_markup(
            reply_markup=await kb.calendar_keyboard(year, month)
        )

@router.callback_query(F.data[0] == "<")
async def previous_month(callback: CallbackQuery) -> None:
    if int(callback.data[1:]) == callback.message.date.month:
        await callback.answer("Превышен лимит")
    else:
        await callback.answer()
        await callback.message.edit_reply_markup(
            reply_markup=await kb.calendar_keyboard(callback.message.date.year, int(callback.data[1:]) - 1)
        )


# @router.message(st.AdminMenuStates.time_slot)
@router.callback_query(F.data[0] == "!")
async def process_time_slot(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(st.AdminMenuStates.time_slot)
    date = str(callback.data)[1:]
    await state.update_data(day_slot=date)
    slots = await rq.get_slots(date=date)
    text = ""
    if len(slots):
        text += f"Доступные слоты <b>{date}</b>: "
        for slot in slots:
            text += f"<b>{slot.time}</b> "
        text += "\n\n❌ Для удаления слота выберите его время"
    
    text += f"\n💅 Для добавления слота на <b>{date}</b> введите время.\nНапример: <b>9:00</b> или <b>18:30</b>."

    msg = await callback.message.edit_text(
        text=text,
        reply_markup=await kb.slots_keyboard(date)
    )    
    await state.update_data(last_message_id=msg.message_id)


@router.callback_query(F.data == "back_to_add_slot")
async def back_to_add_slot(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(st.AdminMenuStates.day_slot)
    await callback.answer()
    await process_day_slot(callback, state)

@router.message(st.AdminMenuStates.time_slot)
async def time_slot(message: Message, state: FSMContext) -> None:
    if not bool(fullmatch(r"0[0-9]:[0-5][0-9]|[0-9]:[0-5][0-9]|1[0-9]:[0-5][0-9]|2[0-3]:[0-5][0-9]", message.text)):
        await delete_last_keyboard(message, state)
        last_msg = await message.answer(
            text="Время введено неправильно, попробуйте ещё раз.",
            reply_markup=await kb.slots_keyboard(await state.get_value("day_slot"))
        )
        await state.update_data(last_message_id=last_msg.message_id)
    else:
        date = await state.get_value("day_slot")
        await rq.add_slot(date=date, time=message.text)
        # await message.bot.edit_message_reply_markup(
        #     chat_id=message.chat.id, message_id=await state.get_value("last_message_id"), reply_markup=None)
        await message.reply(text="✅ Время успешно добавлено")
        await process_day_slot(message, state)
        await state.clear()
        await state.set_state(st.AdminMenuStates.day_slot)


@router.callback_query(F.data[0] == "/")
async def delete_slot(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await rq.delete_slot(date=await state.get_value("day_slot"), time=callback.data[1:])
    await process_day_slot(callback, state)

