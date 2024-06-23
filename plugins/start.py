from datetime import date as date_
import datetime
import os, re
import asyncio
import random
from script import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
from pyrogram import Client, filters, enums
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
import humanize
from helper.progress import humanbytes
from helper.database import botdata, find_one, total_user
from helper.database import insert, find_one, used_limit, usertype, uploadlimit, addpredata, total_rename, total_size
from pyrogram.file_id import FileId
from helper.database import daily as daily_
from helper.date import check_expi
from config import *

bot_username = BOT_USERNAME
log_channel = LOG_CHANNEL
token = BOT_TOKEN
botid = token.split(':')[0]

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.chat.id
    old = insert(int(user_id))

    try:
        id = message.text.split(' ')[1]
    except IndexError:
        id = None

    loading_sticker_message = await message.reply_sticker("CAACAgUAAxkBAAJdZGZjDMwa5Zris5EEemDOnAL1oHa2AAKtCgACa94QV683SZl-OU9gNQQ")
    await asyncio.sleep(2)
    await loading_sticker_message.delete()
    txt=f"""Hello {message.from_user.mention} \n\n➻ This Is An Advanced And Yet Powerful Rename Bot.\n\n➻ Using This Bot You Can Rename And Change Thumbnail Of Your Files.\n\n➻ You Can Also Convert Video To File Aɴᴅ File To Video.\n\n➻ This Bot Also Supports Custom Thumbnail And Custom Caption.\n\n<b>Bot Is Made By @Cs_Bots</b>"""
    await message.reply_photo(photo=BOT_PIC,
                                caption=txt,
                                reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("📢 Updates", url="https://t.me/Cs_Bots"),
                                        InlineKeyboardButton("💬 Support", url="https://t.me/+-LAXtYnqhO1mY2U9")],
                                        [InlineKeyboardButton("🛠️ Help", callback_data='help'),
                                                        InlineKeyboardButton("❤️‍🩹 About", callback_data='about')],
                                        [InlineKeyboardButton("🧑‍💻 Developer 🧑‍💻", url="https://t.me/Cashscopebot")]
                                        ]))
    return

@Client.on_message((filters.private & (filters.document | filters.audio | filters.video)) | filters.channel & (filters.document | filters.audio | filters.video))
async def send_doc(client, message):
    update_channel = FORCE_SUBS
    user_id = message.from_user.id
    if update_channel:
        try:
            await client.get_chat_member(update_channel, user_id)
        except UserNotParticipant:
            _newus = find_one(message.from_user.id)
            user = _newus["usertype"]
            await message.reply_text("<b>Hello Dear \n\nYou Need To Join In My Channel To Use Me\n\nKindly Please Join Channel</b>",
                                     reply_to_message_id=message.id,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("🔺 Update Channel 🔺", url=f"https://t.me/{update_channel}")]]))
            await client.send_message(log_channel,f"<b><u>New User Started The Bot</u></b> \n\n<b>User ID</b> : `{user_id}` \n<b>First Name</b> : {message.from_user.first_name} \n<b>Last Name</b> : {message.from_user.last_name} \n<b>User Name</b> : @{message.from_user.username} \n<b>User Mention</b> : {message.from_user.mention} \n<b>User Link</b> : <a href='tg://openmessage?user_id={user_id}'>Click Here</a> \n<b>User Plan</b> : {user}",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺  Rᴇsᴛʀɪᴄᴛ Usᴇʀ ( **PM** )  🔺", callback_data="ceasepower")]]))
            return

    botdata(int(botid))
    bot_data = find_one(int(botid))
    prrename = bot_data['total_rename']
    prsize = bot_data['total_size']
    user_deta = find_one(user_id)
    used_date = user_deta["date"]
    buy_date = user_deta["prexdate"]
    daily = user_deta["daily"]
    user_type = user_deta["usertype"]

    c_time = time.time()

    if user_type == "Free":
        LIMIT = 5
    else:
        LIMIT = 10
    then = used_date + LIMIT
    left = round(then - c_time)
    conversion = datetime.timedelta(seconds=left)
    ltime = str(conversion)
    if left > 0:
        await message.reply_text(f"<b>Sorry Dude I Am Not Only For You \n\nFlood Control Is Active So Please Wait For {ltime} </b>", reply_to_message_id=message.id)
    else:
        # Forward a single message
        media = await client.get_messages(message.chat.id, message.id)
        file = media.document or media.video or media.audio
        dcid = FileId.decode(file.file_id).dc_id
        filename = file.file_name
        file_id = file.file_id
        value = 2147483648
        used_ = find_one(message.from_user.id)
        used = used_["used_limit"]
        limit = used_["uploadlimit"]
        expi = daily - int(time.mktime(time.strptime(str(date_.today()), '%Y-%m-%d')))
        if expi != 0:
            today = date_.today()
            pattern = '%Y-%m-%d'
            epcho = int(time.mktime(time.strptime(str(today), pattern)))
            daily_(message.from_user.id, epcho)
            used_limit(message.from_user.id, 0)
        remain = limit - used
        if remain < int(file.file_size):
            await message.reply_text(f"100% Of Daily {humanbytes(limit)} Data Quota Exhausted.\n\n<b>File Size Detected :</b> {humanbytes(file.file_size)}\n<b>Used Daily Limit :</b> {humanbytes(used)}\n\nYou Have Only <b>{humanbytes(remain)}</b> Left On Your Account.\n\nIf U Want To Rename Large File Upgrade Your Plan", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💫 Get Free Trial", callback_data="upgrade")]]))
            return
        
        # New logic for DC ID check
        if dcid in [3, 4, 5]:
            copy_message = await client.copy_message(
                chat_id=link_channel,
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=message.caption,
                reply_markup=message.reply_markup
            )
            await message.reply_text(f"**File copied to link channel.**\n\n**DC ID:** {dcid}\n**File Name:** {filename}", reply_to_message_id=message.id)
            return
        
        if value < file.file_size:
            if STRING:
                if buy_date == None:
                    await message.reply_text(f" Yᴏᴜ Cᴀɴ'ᴛ Uᴘʟᴏᴀᴅ Mᴏʀᴇ Tʜᴀɴ 2GB Fɪʟᴇ\n\nYᴏᴜʀ Pʟᴀɴ Dᴏᴇsɴ'ᴛ Aʟʟᴏᴡ Tᴏ Uᴘʟᴏᴀᴅ Fɪʟᴇs Tʜᴀᴛ Aʀᴇ Lᴀʀɢᴇʀ Tʜᴀɴ 2GB\n\nUpgrade Yᴏᴜʀ Pʟᴀɴ Tᴏ Rᴇɴᴀᴍᴇ Fɪʟᴇs Lᴀʀɢᴇʀ Tʜᴀɴ 2GB", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💫 Get Free Trial", callback_data="upgrade")]]))
                    return
                pre_check = check_expi(buy_date)
                if pre_check == True:
                    await message.reply_text(f"""__Wʜᴀᴛ Dᴏ Yᴏᴜ Wᴀɴᴛ Mᴇ Tᴏ Dᴏ Wɪᴛʜ Tʜɪs Fɪʟᴇ ?__\n\n**Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`\n**Fɪʟᴇ Sɪᴢᴇ** :- {humanize.naturalsize(file.file_size)}\n**DC ID** :- {dcid}""", reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Rename", callback_data="rename"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")]]))
                    total_rename(int(botid), prrename)
                    total_size(int(botid), prsize, file.file_size)
                else:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

                    await message.reply_text(f'Yᴏᴜʀ Pʟᴀɴ Exᴘɪʀᴇᴅ Oɴ {buy_date}', quote=True)
                    return
            else:
                await message.reply_text("Yᴏᴜ Cᴀɴ'ᴛ Uᴘʟᴏᴀᴅ Mᴏʀᴇ Tʜᴀɴ 2GB Fɪʟᴇ\n\nYᴏᴜʀ Pʟᴀɴ Dᴏᴇsɴ'ᴛ Aʟʟᴏᴡ Tᴏ Uᴘʟᴏᴀᴅ Fɪʟᴇs Tʜᴀᴛ Aʀᴇ Lᴀʀɢᴇʀ Tʜᴀɴ 2GB\n\nUpgrade Yᴏᴜʀ Pʟᴀɴ Tᴏ Rᴇɴᴀᴍᴇ Fɪʟᴇs Lᴀʀɢᴇʀ Tʜᴀɴ 2GB")
                return
        else:
            if buy_date:
                pre_check = check_expi(buy_date)
                if pre_check == False:
                    uploadlimit(message.from_user.id, 2147483648)
                    usertype(message.from_user.id, "Free")

            filesize = humanize.naturalsize(file.file_size)
            fileid = file.file_id
            total_rename(int(botid), prrename)
            total_size(int(botid), prsize, file.file_size)

            await message.reply_text(f"""__Wʜᴀᴛ Dᴏ Yᴏᴜ Wᴀɴᴛ Mᴇ Tᴏ Dᴏ Wɪᴛʜ Tʜɪs Fɪʟᴇ ?__\n\n**Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`\n**Fɪʟᴇ Sɪᴢᴇ** :- {filesize}\n**DC ID** :- {dcid}""", 
                                        reply_to_message_id=message.id, 
                                        reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton("📝 Rename", callback_data="rename"), InlineKeyboardButton("✖️ Cancel", callback_data="cancel")],
                                            [InlineKeyboardButton("📥 Download", callback_data=f"download_{fileid}")]
                                        ]))

@Client.on_callback_query(filters.regex(r"download_(.*)"))
async def download_file(client, callback_query):
    file_id = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id

    # Fetch messages from link_channel
    messages = await client.get_chat_history(link_channel)
    download_link = None

    # Look for the message containing the file_id and extract the download link
    for msg in messages:
        if msg.reply_markup and msg.document and msg.document.file_id == file_id:
            for button_row in msg.reply_markup.inline_keyboard:
                for button in button_row:
                    if button.url and "fast_link" in button.url:
                        download_link = button.url
                        break
            if download_link:
                break

    if download_link:
        await client.send_message(user_id, f"Download your file from: [Download Link]({download_link})", parse_mode='markdown')
    else:
        await client.send_message(user_id, "Failed to find a download link.")

# Rest of your bot code continues here