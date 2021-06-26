import asyncio

from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message
from userbot.helpers.PyroHelpers import GetChatID


@UserBot.on_message(filters.command("unblock", ".") & filters.me)
async def un_block(_, message: Message):
            text = "`Unblocked!`"

            await UserBot.send_message(text=text, 
                                       reply_to_message_id=message.message_id)
