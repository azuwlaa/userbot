import asyncio

from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message

@UserBot.on_message(filters.command("unblock", ".") & filters.me)
async def un_block(_, message: Message):
    user_first = message.reply_to_message.from_user.first_name
        await add_contact("user_first", "add")
        await message.edit(
                "`UNBLOCKED!`"
            )
