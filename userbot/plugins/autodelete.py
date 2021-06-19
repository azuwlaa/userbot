""
    Werewolf Moderator's autodel for join.
"""
import asyncio
from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message
from userbot.helpers.PyroHelpers import GetChatID

chat_auth = -1001443655011


@UserBot.on_message(filters.regex(r"(?i)Have fun!!!(.*)$"))
async def auto_del_list(_, message: Message):
    
     if chat_auth == GetChatID(message):
        text = ".pin loud"

        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=text, reply_to_message_id=message.message_id)
        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=f"Auto deleted.")

       
