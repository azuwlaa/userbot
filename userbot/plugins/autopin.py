import asyncio

from pyrogram import filters
from pyrogram.methods.chats.get_chat_members import Filters as ChatMemberFilters
from pyrogram.types import Message, ChatPermissions

from userbot import UserBot
from userbot.plugins.help import add_command_help



@UserBot.on_message(filters.command("pin", ".") & filters.me)
