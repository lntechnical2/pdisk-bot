from pyrogram import Client, filters
from time import time
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup 
from datetime import datetime
from pyrogram.types import (
    ForceReply
)
from pdisk import pdisk_url , api_check
from database import insert , find , set , getid
import os

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

TOKEN = os.environ.get("TOKEN", "")
API_ID = int(os.environ.get("API_ID",12345))
API_HASH = os.environ.get("API_HASH","")
ADMIN = os.environ.get("ADMIN",923943045)

app = Client("pdisk" ,bot_token = TOKEN ,api_id = API_ID ,api_hash = API_HASH )
    
@Client.on_message(filters.command("start"))
async def start(client, m: message):
   if m.chat.type == 'private':
       insert(int(m.chat.id))
       await m.reply_text(f"**Hello i am Pdisk Uploader Bot\nMade with love by @mrlokaman`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                     InlineKeyboardButton(
                                            "📢 Bot Updates", url="https://t.me/lntechnical")
                                    ]]
                            ))
   else:
      await m.reply_text(f"**Hola, Join @lntechnical!**")

@app.on_message(filters.private & filters.command(['connect']))
async def connect(client,message):
	await message.reply_text('Send Me Your api_key from pdisk\nhttps://www.cofilink.com/use-api',reply_to_message_id = message.message_id,reply_markup=ForceReply(True))

@Client.on_message(filters.command("ping"))
async def ping_pong(client, m: message):
    start = time()
    m_reply = await m.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(filters.command("uptime"))
async def get_uptime(client, m: message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
	
@app.on_message(filters.private & filters.reply)
async def api_connect(client,message):
        if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        	API_KEY = message.text
        	res = api_check(str(API_KEY))
        	try:
        		check = res['data']
        		set(message.chat.id,API_KEY)
        		await message.reply_text("Your Account Conected Successfully ✅",reply_to_message_id = message.message_id)
        	except Exception as f:
        		print(f)
        		e = res['msg']
        		await message.reply_text(f"Error: {e}",reply_to_message_id = message.message_id)


@app.on_message(filters.private & filters.user(ADMIN) & filters.command(["broadcast"]))
async def broadcast(client,message):
 if (message.reply_to_message):
   text_reply = await message.reply_text("fetching users from database")
   users = getid()
   total = len(ids)
   await text_reply.edit(f"Broadcast Succesfully Started\n\nSending Message To {total} Users")
   for id in users:
     try:
     	await message.reply_to_message.copy(id)
     except:
     	pass       		       	

@app.on_message(filters.private & filters.regex("http|https"))
async def upload(client,message):
	api_key = find(message.chat.id)
	if api_key:
		data = message.text
		v_ = data.split("\n")
		try:
			title = v_[0].split('-')[1]
			link  = v_[1].split('-')[1].replace(" ","")
		except :
			await message.reply_text('**How To Use**\n\nExample:-\n```title - Sample test \nlink - http://telegramfiles.com/files/10384867/6096083c4f62cba7367b9b6891bafd98/10_Minute_Timer_4ASKMcdCc3g_278.mkv\ntumb - https://tgstream.iamidiotareyoutoo.com/159180/1875203403```\n\n**thumb is optinal you can send titlt and link**',reply_to_message_id = message.message_id)
			return
		try:
			thumb =  v_[2].split('-')[1].replace(" ","")
		except:
			thumb = None
		if thumb:
			res = pdisk_url(api_key,link,title,thumb)
			try:
				id = res['data']['item_id']
				await message.reply_text(f'Title : {title}\n\nURL : ```https://cofilink.com/share-video?videoid={id}```\n\n**This File Will Be Uploading in  10 - 15 Minutes **',reply_to_message_id = message.message_id)
			except:
				e = res['msg']
				await message.reply_text(f"Error: ```{e}```",reply_to_message_id = message.message_id)
		else:
			pdisk_url(api_key,link,title)
			try:
				id = res['data']['item_id']
				await message.reply_text(f'Title : {title}\nURL:```https://cofilink.com/share-video?videoid={id}```\n This File Will Be Uploading in  10 - 15 Minutes ',reply_to_message_id = message.message_id)
			except:
				e = res['msg']
				await message.reply_text(f"Error:```{e}```",reply_to_message_id = message.message_id)
			
	else:
		await message.reply_text("Connect Your Account Using Command /connect",reply_to_message_id = message.message_id)	
		
app.run()
