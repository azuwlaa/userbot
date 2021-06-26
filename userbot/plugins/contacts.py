import asyncio

from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message

@UserBot.add_contact(filters.command("unblock", ".") & filters.me)
async def add_contact(_, message: Message):
    if message.reply_to_message is None:
        await message.edit(
                "`WHO SHOULD I UNBLOCK?`"
            )
        return
    else:
        replied_user = message.reply_to_message.from_user
        await message.edit(
                "`UNBLOCKED!`"
            )
