from telethon import events, types, functions
from userbot import bot, OWNER_ID   # make sure OWNER_ID exists in userbot config


# Helper — owner only
def is_owner(event):
    return event.sender_id == OWNER_ID


# =========================
#   ADD CONTACT (reply)
#   .addc nickname
# =========================
@bot.on(events.NewMessage(pattern=r"\.addc(?: |$)(.*)"))
async def add_contact(event):
    if not is_owner(event):
        return  # ignore others

    nickname = event.pattern_match.group(1).strip()

    if not event.is_reply:
        return await event.reply("⚠ Reply to someone's message.\nUsage: `.addc nickname`")

    reply = await event.get_reply_message()
    user = await reply.get_sender()

    if not nickname:
        nickname = user.first_name or "Unknown"

    status = await event.reply("📥 **Adding this person to your contacts…**")

    try:
        await bot(functions.contacts.ImportContactsRequest(
            contacts=[types.InputPhoneContact(
                client_id=0,
                phone=user.phone or "",
                first_name=nickname,
                last_name=""
            )]
        ))

        await status.edit(f"📇 **Contact added:** {nickname}\n👤 User: `{user.id}`")

    except Exception as e:
        await status.edit(f"❌ Error: `{e}`")



# =========================
#   REMOVE CONTACT (reply)
#   .rmc
# =========================
@bot.on(events.NewMessage(pattern=r"\.rmc$"))
async def remove_contact(event):
    if not is_owner(event):
        return

    if not event.is_reply:
        return await event.reply("⚠ Reply to someone's message.\nUsage: `.rmc`")

    reply = await event.get_reply_message()
    user = await reply.get_sender()

    status = await event.reply("🗑 **Removing this contact…**")

    try:
        await bot(functions.contacts.DeleteContactsRequest(
            id=[types.InputUser(user.id, user.access_hash)]
        ))

        await status.edit(f"🗑 **Contact removed:** `{user.id}`")

    except Exception as e:
        await status.edit(f"❌ Error: `{e}`")



# =========================
#   RENAME CONTACT (reply)
#   .renamec NewName
# =========================
@bot.on(events.NewMessage(pattern=r"\.renamec(?: |$)(.*)"))
async def rename_contact(event):
    if not is_owner(event):
        return

    new_name = event.pattern_match.group(1).strip()

    if not event.is_reply:
        return await event.reply("⚠ Reply to someone's message.\nUsage: `.renamec NewName`")

    if not new_name:
        return await event.reply("⚠ Type a new name.\nUsage: `.renamec NewName`")

    reply = await event.get_reply_message()
    user = await reply.get_sender()

    status = await event.reply("✏ **Renaming this contact…**")

    try:
        await bot(functions.contacts.ImportContactsRequest(
            contacts=[types.InputPhoneContact(
                client_id=0,
                phone=user.phone or "",
                first_name=new_name,
                last_name=""
            )]
        ))

        await status.edit(f"✏ **Contact renamed to:** {new_name}\n👤 User: `{user.id}`")

    except Exception as e:
        await status.edit(f"❌ Error: `{e}`")
