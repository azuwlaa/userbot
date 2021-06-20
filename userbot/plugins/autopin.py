"""
    Werewolf Moderator's autopin for players list.
"""
import asyncio
from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message
from userbot.helpers.PyroHelpers import GetChatID


CHAT_AUTH = [-1001443655011]  # add chat ids without quotes


@UserBot.on_message(filters.regex(r"(?i)#players:(.*)$"))
async def auto_pin_list(_, message: Message):
    chat_id = GetChatID(message) 
    if chat_id in CHAT_AUTH:
        text = ".pin loud"

        await UserBot.send_message(chat_id=chat_id,
                                   text=text, reply_to_message_id=message.message_id)
        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=f"This is an auto-pin.")
        await asyncio.sleep(3)
        await message.delete()


@UserBot.on_message(filters.regex(r"(?i)Game Length:(.*)$") | filters.regex(r"(?i)Not enough players,(.*)$"))
async def auto_unpin_list(_, message: Message):
    chat_id = GetChatID(message)
    
    if chat_id in CHAT_AUTH:
        text = ".unpin"
        await UserBot.send_message(chat_id=chat_id,
                                   text=text)


@UserBot.on_message(filters.regex(r"(?i)There is no game running. (.*)$"))
async def auto_del_list(_, message: Message):
    chat_id = GetChatID(message)
    if chat_id in CHAT_AUTH:
        text = ".del"

        await UserBot.send_message(chat_id=chat_id,
                                   text=text, reply_to_message_id=message.message_id)
        await UserBot.send_message(chat_id=chat_id,
                                   text=f"This is an auto-del.")
        await asyncio.sleep(3)
        await message.delete()

@UserBot.on_message(filters.regex(r"(?i)Have fun!!!(.*)$"))
async def auto_del_list(_, message: Message):
    chat_id = GetChatID(message)
    if chat_id in CHAT_AUTH:
        text = ".del"

    await UserBot.send_message(chat_id=chat_id,
                               text=text, reply_to_message_id=message.message_id)
    await UserBot.send_message(chat_id=chat_id,
                               text=f"This is an auto-del.")
    await asyncio.sleep(3)
    await message.delete()
