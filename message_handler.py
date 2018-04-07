import discord
import asyncio

#return global vars with functions names
def getGlobals():
	return globals()


#Multiline Quote
async def quote_multiline(client, message, opt_commands):
	print("quote_multiline()")
	import quoting_multiline as qm

	print("Quoting Multiline has imported")
	quotm = qm.Quoting(client, message, opt_commands)
	await quotm.preload()
	

#send your message from bot
async def message_from_bot(client, message):
	print("message_from_bot()")
	content = message.content
	await client.delete_message(message)
	await client.send_message(message.channel, content = content)
