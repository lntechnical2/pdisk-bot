from pyrogram import Client, filters

@Client.on_message(filters.private &(filters.document | filters.video))
async def file_down(client,message):
	file = message
	ms = await message.repy_text("``` Trying To Download...```")
	try:
	   path = await client.download_media(message = file)
	   await ms.edit(f"{path}")
	except Exception as e:
		await ms.edit(e)
