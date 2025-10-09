# from aiogram import BaseMiddleware
# from aiogram.types import Message
# from aiogram.fsm.storage.base import BaseStorage, StorageKey

# from typing import Callable, Any, Dict, Awaitable

# class DeleteKeyboard(BaseMiddleware):
#     def __init__(self, storage: BaseStorage):
#         super().__init__()
#         self.storage = storage

#     async def __call__(self,
#                        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#                        event: Message,
#                        data: Dict[str, Any]) -> Any:
#         dp = data.get("dispatcher")
#         user_id = event.from_user.id
#         chat_id = event.chat.id

#         key = StorageKey(bot_id=event.bot.id, chat_id=chat_id, user_id=user_id)
#         last_message_id = await self.storage.get_value(key, "last_message_id")
#         print(last_message_id)
#         if last_message_id:
#             await event.bot.edit_message_reply_markup(
#             chat_id=event.chat.id, message_id=last_message_id, reply_markup=None
#             )
#         result = await handler(event, data)
#         return result

