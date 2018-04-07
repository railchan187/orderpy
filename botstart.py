import sys
import copy

import discord
import asyncio

import importlib

import message_handler as mh


client = discord.Client()


try:
	import json

	with open("config.json") as config:
			config = json.load(config)

	token 				= config['token']
	botname				= config['botname']
	playgame			= config['playgame']

	bot_prefixes 		= config['bot_prefixes']
	bot_short_commands 	= config['bot_short_commands']
	opt_commands 		= config['opt_commands']

	_globals = mh.getGlobals()
	_globals.update(globals())

	#switch-case
	#keys - startwith of message
	#values - functions from message_handler.py
	switcher = {}
	for key, value in config['switcher'].items():
		switcher[key] = _globals[value]


except:
	print("Config file not found!")
	sys.exit()



@client.event
async def on_ready():
	print("{} is ready!".format(botname))
	print("Name: {}".format(client.user.name))
	print("ID: {}".format(client.user.id))
	print("---------------------------------")

	await client.change_presence(game = discord.Game(name = playgame))


@client.event
async def on_message(message):
	
	print('\n')
	print('Message info:')
	print('---------------------------------')
	print('author: {}'.format(message.author))
	print('id: {}'.format(message.author.id))
	print('server: {}'.format(message.server))
	print('channel: {}'.format(message.channel))
	print('content: {}'.format(message.content))

	try:
		ind = 1
		for emb in message.embeds:
			print('emb{} description: {}'.format(ind, emb['description']))	
	except:
		pass
	
	print('---------------------------------')
	print('\n')

	#bot found the commands in message
	if any(message.content.lower().startswith(prefix) for prefix in bot_prefixes):
		await start_handler(message)
	if any(message.content.lower().startswith(cmd) for cmd in bot_short_commands):
		await start_handler(message, short = True)
	

#Start message_handler
async def start_handler(message, short = False):

	#Calling func from switcher

	#using command with bot_prefix
	if short == False:
		mess_startwith = message.content.lower().split()
		if len(mess_startwith) > 1 and mess_startwith[1] in switcher:
			message_without_cmd = del_cmd_from_message_content(message, short)
			await switcher[mess_startwith[1]](client, message_without_cmd)
			
	#using short command without bot_prefix
	if short == True:
		mess_startwith = message.content.lower().split()
		if len(mess_startwith) > 0 and mess_startwith[0] in switcher:
			message_without_cmd = del_cmd_from_message_content(message, short)
			
			
			#Call funcs with Special Arguments

			#mh.quote_multiline
			if switcher[mess_startwith[0]] == mh.quote_multiline:
				await switcher[mess_startwith[0]](client, message_without_cmd, opt_commands)	
				return
			
			#else
			await switcher[mess_startwith[0]](client, message_without_cmd)


#Delete in message.content command and return message without one
def del_cmd_from_message_content(message, short = True):

	lines = message.content.split('\n')
	
	if short == False:
		lines[0] = " ".join(lines[0].split()[2:])
	if short == True:
		lines[0] = " ".join(lines[0].split()[1:])
	
	content = "\n".join(lines)

	message.content = content
	#print('content: {}'.format(content))

	return message
	

client.run(token)

