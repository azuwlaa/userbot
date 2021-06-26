import asyncio

from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message

@UserBot.on_message(filters.command("unblock", ".") & filters.me)
async def add_contact(_, message: Message):
    user_first = message.reply_to_message.from_user.first_name
    if message.reply_to_message is None:
        await message.edit(
                "`WHO SHOULD I UNBLOCK?`"
            )
        return
    else:
        Replied_user = UserBot.add_contact("username")
        await message.edit(
                "`UNBLOCKED!`"
            )
