import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from helper.utils import find_one, humanbytes, FileId
from config import log_channel, LINK_CHANNEL

logging.basicConfig(level=logging.INFO)

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user_id = message.from_user.id
    txt = (
        "Hello! I am a simple file renamer bot.\n\n"
        "➻ I can rename any file without downloading it!\n\n"
        "➻ Just send me any file or video to get started.\n\n"
        "➻ Also, this bot can extract media from channel links."
    )
    await message.reply_photo(
        photo="https://telegra.ph/file/ff4b5b23391f3558f9e24.jpg",
        caption=txt,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💠 Support Group", url="https://t.me/YourSupportGroup"),
                    InlineKeyboardButton("📣 Updates Channel", url="https://t.me/YourUpdatesChannel"),
                ]
            ]
        ),
    )

    if log_channel:
        await client.send_message(log_channel, f"#NewUser\n\nUser ID: `{user_id}`\nStarted Your Bot!")

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def send_doc(client, message):
    user_id = message.from_user.id
    bot_data = find_one(user_id)

    if not bot_data:
        await message.reply_text("You are not authorized to use this bot.")
        return

    try:
        file = message.document or message.video or message.audio
        dcid = FileId.decode(file.file_id).dc_id

        if dcid in [1, 2]:
            await message.reply_text("This file cannot be copied because its DC ID is 1 or 2.")
            return

        await message.reply_text(
            f"**What do you want to do with this file?**\n\n"
            f"File Name: `{file.file_name}`\nFile Size: `{humanbytes(file.file_size)}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Rename", callback_data="rename")],
                    [InlineKeyboardButton("Extract from Link", callback_data="vid")]
                ]
            ),
            quote=True
        )
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run()