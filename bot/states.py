from aiogram.fsm.state import StatesGroup, State


class RegisterUser(StatesGroup):
    name = State()
    phonenumber = State()

class UserMenuStates(StatesGroup):
    main_menu = State()
    account_menu = State()
    service_menu = State()

    change_name = State()

    isAdmin= State()
    mode = State()
    
    last_message_id = State()

class AdminMenuStates(StatesGroup):

    day_slot = State()
    time_slot = State()
