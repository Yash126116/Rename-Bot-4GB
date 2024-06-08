from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from pyrogram import Client , filters

@Client.on_callback_query(filters.regex('upgrade'))
async def upgrade(bot,update):
	text = """**Free Plan User**
	Daily  Upload limit 10TB ~ Unlimited 
	Price 0
	
	**🪙 Basic** 
	Daily  Upload  limit 10GB
	Pric 🌎 0.5$  per Month
	
	**⚡ Standard**
	Daily Upload limit 50GB
	Price 🌎 1$  per Month
	
	**💎 Pro**
	Daily Upload limit 100GB
	Price 🌎 1.5$  per Month
	
	
	Pay Using Binance Pay I'd `185823678`
	
	After Payment Send Screenshots Of 
        Payment To Admin @Cashscopebot"""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Admin",url = "https://t.me/Cashscopebot")], 
        			[InlineKeyboardButton("Phone Pay",url = "https://graph.org/file/8193b7e8d969f8db28ab2.jpg"),
        			InlineKeyboardButton("Paytm Wallet/UPI",url = "https://graph.org/file/8193b7e8d969f8db28ab2.jpg")],[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)
	

@Client.on_message(filters.private & filters.command(["upgrade"]))
async def upgradecm(bot,message):
	text = """**Free Plan User**
	Daily  Upload limit 10TB ~ Unlimited 
	Price 0
	
	**🪙 Basic** 
	Daily  Upload  limit 20GB
	Price 🌎 0.5$  per Month
	
	**⚡ Standard**
	Daily Upload limit 50GB
	Price 🌎 1$  per Month
	
	**💎 Pro**
	Daily Upload limit 100GB
	Price 🌎 1.5$  per Month
	
	
	Pay Using Binance Pay I'd `185823678`
	
	After Payment Send Screenshots Of 
        Payment To Admin @Cashscopebot"""
	keybord = InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Admin",url = "https://t.me/Cashscopebot")], 
        			[InlineKeyboardButton("Phone Pay",url = "https://graph.org/file/8193b7e8d969f8db28ab2.jpg"),
        			InlineKeyboardButton("Paytm Wallet/UPI",url = "https://graph.org/file/8193b7e8d969f8db28ab2.jpg")],[InlineKeyboardButton("Cancel",callback_data = "cancel")  ]])
	await update.message.edit(text = text,reply_markup = keybord)