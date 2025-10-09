from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter, Command
from aiogram.exceptions import TelegramBadRequest


import bot.keyboards.keyboard as kb
import bot.datebase.requests as rq
import bot.states.states_user as st
from bot.handlers.user import delete_last_keyboard

from settings import settings



router = Router()

# class AdminFilter(BaseFilter):
#     async def __call__(self, event: Message|CallbackQuery):
#         return event.from_user.id in settings.ADMINS

# @router.message(Command(commands=["admin"]), AdminFilter())
# async def admin_panel(message: Message) -> None:
#     await message.answer("Hi admin!")

@router.message(st.AdminMenuStates.add_slot)
@router.callback_query(F.data == "add_slot", st.UserMenuStates.main_menu)
async def process_name_slot(event: Message|CallbackQuery, state: FSMContext) -> None:
    text = "Выбери нужные даты:"
    if isinstance(event, Message):
        await delete_last_keyboard(event, state)
        last_msg = await event.answer(
            text=text,
            reply_markup=await kb.calendar_keyboard(event.date.year, event.date.month)
        )
        await state.update_data(last_message_id=last_msg.message_id)
    else:
        await state.set_state(st.AdminMenuStates.add_slot)
        await event.answer()
        await event.message.edit_text(
            text=text,
            reply_markup=await kb.calendar_keyboard(event.message.date.year, event.message.date.month)
        )


@router.callback_query(F.data == "_")
async def quick_callback(callback: CallbackQuery) -> None:
    await callback.answer()


@router.callback_query(F.data[-1] == ">")
async def next_moth(callback: CallbackQuery) -> None:
    if int(callback.data[:-1]) > callback.message.date.month:
        await callback.answer("Превышен лимит(")
    else:
        await callback.answer()
        await callback.message.edit_reply_markup(
            reply_markup=await kb.calendar_keyboard(callback.message.date.year, int(callback.data[:-1]) + 1)
        )

@router.callback_query(F.data[-1] == "<")
async def previous_month(callback: CallbackQuery) -> None:
    if int(callback.data[:-1]) == callback.message.date.month:
        await callback.answer("Превышен лимит(")
    else:
        await callback.answer()
        await callback.message.edit_reply_markup(
            reply_markup=await kb.calendar_keyboard(callback.message.date.year, int(callback.data[:-1]) - 1)
        )
