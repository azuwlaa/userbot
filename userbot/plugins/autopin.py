"""
    Werewolf Moderator's autopin for players list.
"""
import asyncio
from userbot import UserBot
from pyrogram import filters
from pyrogram.types import Message
from userbot.helpers.PyroHelpers import GetChatID

chat_auth = -1001443655011


@UserBot.on_message(filters.regex(r"(?i)#players:(.*)$"))
async def auto_pin_list(_, message: Message):
    
     if chat_auth == GetChatID(message):
        text = ".pin loud"

        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=text, reply_to_message_id=message.message_id)
        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=f"This is an auto-pin.")


@UserBot.on_message(filters.regex(r"(?i)Game Length:(.*)$"))
async def auto_unpin_list(_, message: Message):
     if chat_auth == GetChatID(message):
        text = ".unpin"
        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=text)
        
        
@UserBot.on_message(filters.regex(r"(?i)There is no game running. (.*)$"))
async def auto_del_list(_, message: Message):
    
     if chat_auth == GetChatID(message):
        text = ".del"

        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=text, reply_to_message_id=message.message_
        
       
@UserBot.on_message(filters.regex(r"(?i)Have fun!!!(.*)$"))
async def auto_del_list(_, message: Message):
    
     if chat_auth == GetChatID(message):
        text = ".del"

        await UserBot.send_message(chat_id=GetChatID(message),
                                   text=text, reply_to_message_id=message.message_id)


       
