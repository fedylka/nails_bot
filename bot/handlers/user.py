import re

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

import bot.states.states_user as st
import bot.keyboards.keyboard as kb
import bot.datebase.requests as rq

# from settings import settings 


router = Router()


#Регистрация нового пользователя
@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if not (await rq.get_user(message.from_user.id)):
        await state.set_state(st.RegisterUser.name)
        await message.answer("Привет! Давай пройдём короткую регистрацию.")
        await message.answer("Как мне к тебе обращаться?\nНапиши своё имя:")
    else:
        await state.set_state(st.UserMenuStates.main_menu)
        await main_menu(message, state)

@router.message(st.RegisterUser.name)
async def process_name(message: Message, state: FSMContext) -> None:
    name = message.text
    if len(name) > 16:
        await message.answer("Слишком длинное. Попробуй ещё раз:")
    elif not bool(re.fullmatch(r"[a-zA-Zа-яА-ЯёЁ\s\-]+", name)):
        await message.answer("Недопустимые символы. Попробуй ещё раз:")
    else:
        await state.update_data(name=name)
        await state.set_state(st.RegisterUser.phonenumber)
        await message.answer(f"Отлично {name}, теперь отправь мне свой номер.", reply_markup=kb.get_number_keyboard)

@router.message(st.RegisterUser.phonenumber)
async def process_number(message: Message, state: FSMContext) -> None:
    try:
        phonenumber = message.contact.phone_number 
        phonenumber = "+" + phonenumber if phonenumber[0] != "+" else phonenumber       
        await state.update_data(phonenumber=phonenumber)
        data = await state.get_data()
        await rq.add_user(
            tg_id=message.from_user.id,
            name=data["name"], 
            phonenumber=data["phonenumber"],
            isAdmin=True#bool(message.from_user.id in settings.ADMINS)
        )
        await state.clear()  
        await state.set_state(st.UserMenuStates.main_menu)
        # await state.update_data(isAdmin=bool(message.from_user.id in settings.ADMINS), mode=False)

        await message.answer("Регистрация прошла успешно! Твои данные сохранены.", reply_markup=ReplyKeyboardRemove())
        await main_menu(message, state)

    except AttributeError:
        await message.answer("Нажмите на кнопку 'Поделиться контактом'.")


async def delete_last_keyboard(event: Message, state: FSMContext) -> None:
    last_message_id = await state.get_value("last_message_id")
    if last_message_id:
        await event.bot.edit_message_reply_markup(
        chat_id=event.chat.id, message_id=last_message_id, reply_markup=None
        )


@router.message(st.UserMenuStates.main_menu)
@router.callback_query(F.data == "back_to_main_menu")
async def main_menu(event: Message|CallbackQuery, state: FSMContext) -> None:
    text = "<b>Главное Меню</b>\n\n        👇Выбери нужное действие👇"
    isAdmin = await state.get_value("isAdmin")
    mode = await state.get_value("mode")
    if isAdmin is None or mode is None:
        # isAdmin = bool(event.from_user.id in settings.ADMINS)
        mode = False
        await state.update_data(isAdmin=isAdmin, mode=mode)    
    if isinstance(event, Message):
        await delete_last_keyboard(event, state)
        last_msg = await event.answer(text=text, reply_markup=await kb.main_menu_keyboard(isAdmin=isAdmin, mode=mode))
        await state.update_data(last_message_id=last_msg.message_id)
    else:
        await event.answer()
        await state.set_state(st.UserMenuStates.main_menu)
        await event.message.edit_text(text=text, reply_markup=await kb.main_menu_keyboard(isAdmin=isAdmin, mode=mode))

@router.message(st.UserMenuStates.main_menu)
@router.callback_query(F.data == "change_mode")
async def change_mode(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await rq.change_mode_user(tg_id=callback.from_user.id)
    isAdmin = await state.get_value("isAdmin")
    mode = await state.get_value("mode")
    if isAdmin is None or mode is None:
        # isAdmin = bool(callback.from_user.id in settings.ADMINS)
        mode = False
        await state.update_data(isAdmin=isAdmin, mode=~mode)
        
    await state.update_data(mode=~mode)
    await callback.message.edit_reply_markup(
        reply_markup=await kb.main_menu_keyboard(isAdmin=isAdmin, mode=~mode)
    )


@router.message(st.UserMenuStates.account_menu)
@router.callback_query(F.data == "to_account")
async def process_account(event: Message|CallbackQuery, state: FSMContext) -> None:
    user: rq.User = await rq.get_user(tg_id=event.from_user.id)
    text = f"Имя: {user.name}\nНомер телефона: {user.phonenumber}"
    if isinstance(event, Message):
        await delete_last_keyboard(event, state)
        last_msg = await event.answer(text=text, reply_markup=kb.account_menu_keyboard)
        await state.update_data(last_message_id=last_msg.message_id)
    else:
        await event.answer()
        await state.set_state(st.UserMenuStates.account_menu)
        await event.message.edit_text(text=text, reply_markup=kb.account_menu_keyboard)

@router.callback_query(F.data == "change_name")
async def change_name_process(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(st.UserMenuStates.change_name)
    await callback.message.edit_text("Отправь мне своё новое имя:", reply_markup=None)

@router.message(st.UserMenuStates.change_name)
async def change_name_complite(message: Message, state: FSMContext) -> None:
    await rq.update_name_user(tg_id=message.from_user.id, new_name=message.text)
    await state.set_state(st.UserMenuStates.account_menu)
    await message.answer(text="Имя успешно изменено.")
    await process_account(message, state)