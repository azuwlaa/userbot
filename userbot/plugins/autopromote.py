"""
     Module to promote yourself to admin.
"""
import asyncio
from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message
from userbot.helpers.PyroHelpers import GetChatID


CHAT_AUTH = [-1001421604603]  # add chat ids without quotes


@UserBot.on_message(filters.regex(r"(?i)promoteme(.*)$"))
async def auto_pro_admin(_, message: Message):
    chat_id = GetChatID(message) 
    if chat_id in CHAT_AUTH:
        text = "`You're already an admin!`"

        await UserBot.send_message(chat_id=chat_id,
                                   text=text, reply_to_message_id=message.message_id)


               
