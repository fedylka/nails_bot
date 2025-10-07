from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter, Command
from aiogram.exceptions import TelegramBadRequest


import bot.keyboards.keyboard as kb
import bot.datebase.requests as rq
import bot.states.states_user as st

from settings import settings

router = Router()

# class AdminFilter(BaseFilter):
#     async def __call__(self, event: Message|CallbackQuery):
#         return event.from_user.id in settings.ADMINS

# @router.message(Command(commands=["admin"]), AdminFilter())
# async def admin_panel(message: Message) -> None:
#     await message.answer("Hi admin!")


@router.callback_query(F.data == "add_slot", st.UserMenuStates.main_menu)
async def process_name_slot(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    print(callback.message.date)
    # last_message_id = await state.get_value("last_message_id")
    # await state.clear()
    # await state.set_state(st.AdminMenuStates.date_slot)
    # await callback.message.edit_text(text="Введите дату.\nПример: 15.02.25")
    




    

    

