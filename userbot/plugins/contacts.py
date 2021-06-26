import asyncio

from userbot import UserBot
from userbot import User
from pyrogram import filters
from pyrogram.types import Message


@UserBot.on_message(filters.command("unblock", ".") & filters.me)
async def un_block(_, message: Message):
        if chat_id = GetChatID(message) 
            text = "`Unblocked!`"

            await UserBot.send_message(chat_id=chat_id,
                                   text=text, reply_to_message_id=message.message_id)
