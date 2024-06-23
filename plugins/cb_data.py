from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import *
import os
import random
from PIL import Image
import time
from datetime import timedelta
from helper.ffmpeg import take_screen_shot, fix_thumb
from helper.progress import humanbytes
from helper.set import escape_invalid_curly_brackets
from config import *

log_channel = LOG_CHANNEL
link_channel = LINK_CHANNEL
app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot, update):
    try:
        await update.message.delete()
    except:
        return

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    date_fa = str(update.message.date)
    pattern = '%Y-%m-%d %H:%M:%S'
    date = int(time.mktime(time.strptime(date_fa, pattern)))
    chat_id = update.message.chat.id
    id = update.message.reply_to_message_id
    await update.message.delete()
    await update.message.reply_text(f"__Please Enter The New Filename...__\n\nNote:- Extension Not Required", reply_to_message_id=id, reply_markup=ForceReply(True))
    dateupdate(chat_id, date)

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

@Client.on_callback_query(filters.regex("vid"))
async def vid(bot, update):
    new_name = update.message.text
    used_ = find_one(update.from_user.id)
    used = used_["used_limit"]
    date = used_["date"]
    name = new_name.split(":-")
    new_filename = name[1]
    file_path = f"downloads/{new_filename}"
    message = update.message.reply_to_message
    file = message.document or message.video or message.audio
    ms = await update.message.edit("`Trying to download...`")
    used_limit(update.from_user.id, file.file_size)
    c_time = time.time()
    total_used = used + int(file.file_size)
    used_limit(update.from_user.id, total_used)
    try:
        path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=("`Trying to download...`", ms, c_time))
    except Exception as e:
        neg_used = used - int(file.file_size)
        used_limit(update.from_user.id, neg_used)
        await ms.edit(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name = f"downloads/{dow_file_name}"
    os.rename(old_file_name, file_path)
    user_id = int(update.message.chat.id)
    data = find(user_id)
    try:
        c_caption = data[1]
    except:
        pass
    thumb = data[0]

    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    if c_caption:
        vid_list = ["filename", "filesize", "duration"]
        new_tex = escape_invalid_curly_brackets(c_caption, vid_list)
        caption = new_tex.format(filename=new_filename, filesize=humanbytes(file.file_size), duration=timedelta(seconds=duration))
    else:
        caption = f"**{new_filename}**"
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()
    else:
        try:
            ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
            width, height, ph_path = await fix_thumb(ph_path_)
        except Exception as e:
            ph_path = None
            print(e)

    value = 2090000000
    if value < file.file_size:
        await ms.edit("`Trying to upload...`")
        try:
            filw = await app.send_video(log_channel, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying to upload...`", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                pass
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(e)
            os.remove(file_path)
            try:
                os.remove(ph_path)
            except:
                return
    else:
        await ms.edit("`Trying to upload...`")
        c_time = time.time()
        try:
            filw = await bot.send_video(log_channel, video=file_path, thumb=ph_path, duration=duration, caption=caption, progress=progress_for_pyrogram, progress_args=("`Trying to upload...`", ms, c_time))
            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await bot.copy_message(update.from_user.id, from_chat, mg_id)
            await ms.delete()
            os.remove(file_path)
        except Exception as e:
            neg_used = used - int(file.file_size)
            used_limit(update.from_user.id, neg_used)
            await ms.edit(str(e))
            os.remove(file_path)
            return

# Add any additional code or handlers as needed