import asyncio

from userbot import UserBot
from userbot import User
from pyrogram import filters
from pyrogram.types import Message


user_first = message.reply_to_message.from_user.first_name


@UserBot.on_message(filters.command("unblock", ".") & filters.me)
async def un_block(_, message: Message):
        await add_contact("added", reply_to_message_id=user_first)
        await message.edit(
                "`UNBLOCKED!`"
            )
