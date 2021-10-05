from pyrogram import Client, filters
from pyrogram.types import (
    ForceReply
)
from pdisk import pdisk_url , api_check
from database import insert , find , set 
import os


TOKEN = os.environ.get("TOKEN", "")

API_ID = int(os.environ.get("APP_ID", "12345"))

API_HASH = os.environ.get("API_HASH", "")

app = Client(
        "pdisk_bot",
        bot_token=TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
    )
    
@app.on_message(filters.private & filters.command(["start"]))
async def start(client,message):
	insert(int(message.chat.id))
	await message.reply_text("Hello iam Pdisk Uploader Bot\nMade with love by @mrlokaman")

@app.on_message(filters.private & filters.command(['connect']))
async def connect(client,message):
	await message.reply_text('Send Me Your api_key from pdisk\nhttps://www.cofilink.com/use-api',reply_markup=ForceReply(True))
	            

@Client.on_message(filters.private & filters.reply)
async def api_connect(client,message):
        if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        	API_KEY = message.text
        	res = api_check(str(API_KEY))
        	try:
        		check = res['data']
        		set(message.chat.id,API_KEY)
        		await message.reply_text("Your Account Conected Successfully ✅")
        	except:
        		e = res['msg']
        		await message.reply_text("Error:{e}")

        		       	

@app.on_message(filters.private & filters.regex("http|https"))
async def upload(client,message):
	api_key = find(message.chat.id)
	if ap_key:
		data = message.text
		v_ = data.split("\n")
		try:
			title = v_[0].split('-')[1]
			link  = v_[1].split('-')[1].replace(" ","")
		except :
			await message.reply_text('**How To Use**\nExample:-\n```title - Sample test \nlink - http://telegramfiles.com/files/10384867/6096083c4f62cba7367b9b6891bafd98/10_Minute_Timer_4ASKMcdCc3g_278.mkv\ntumb - https://tgstream.iamidiotareyoutoo.com/159180/1875203403```\nthumb is optinal you can send titlt and link')
			return
		try:
			thumb =  v_[0].split('-')[1].replace(" ","")
		except:
			thumb = None
		if thumb:
			res = pdisk_url(api_key,link,title,thumb)
			try:
				id = res['data']['item_id']
				await message.reply_text(f'Title : {title}\nURL:```https://cofilink.com/share-video?videoid={id}```\n This File Will Be Uploading in  10 - 15 Minutes ')
			except:
				e = res['msg']
				await message.reply_text(f"Error:```{e}```")
		else:
			pdisk_url(api_key,link,title)
			try:
				id = res['data']['item_id']
				await message.reply_text(f'Title : {title}\nURL:```https://cofilink.com/share-video?videoid={id}```\n This File Will Be Uploading in  10 - 15 Minutes ')
			except:
				e = res['msg']
				await message.reply_text(f"Error:```{e}```")
			
	else:
		await message.reply_text("Connect Your Account Using Command /connect")						
