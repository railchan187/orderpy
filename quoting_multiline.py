import discord
import asyncio

from BondMessagesModule import BondMessages

class Quoting:

	#Init variables
	def __init__(self, client, message, opt_commands):
		self.client   			= client
		self.message  			= message
		self.receiver			= None
		self.opt_commands 		= opt_commands

		print("Quoting init complete")


	async def preload(self):
		test_message = self.message
		
		print('\n')
		print("+++++++TEST_BLOCK++++++++")
		print('author: {}'.format(test_message.author))
		print('id: {}'.format(test_message.author.id))
		print('server: {}'.format(test_message.server))
		print('channel: {}'.format(test_message.channel))
		print('content: {}'.format(test_message.content))
		print("+++++++++++++++++++++++++")
		print('\n')

		await self.body()
		self.endload()


	async def body(self):		
		
		#Divideы content into quote and anser
		self.message.content, answer_text = self.findAnswerBlock()

		#Bonds messages
		bond_messages = await self.bondingMessages()
		
		#Founded quote and author
		result_quote, self.receiver = bond_messages.findTheQuote(self.message.content)

		if (result_quote == None):
			print("Nothing found")
			return
		
		print("result_quote: ", result_quote)
		await self.createQuote(result_quote, answer_text)


	def endload(self):
		pass


	#Finds answer text
	def findAnswerBlock(self):
		answer_text = None
		content = self.message.content
		s_ind = -1

		for opt in self.opt_commands:
			s_ind = max(content.lower().rfind(opt+' '), content.lower().rfind(opt+'\n'))
			if s_ind != -1:
				break

		if (s_ind != -1 ):
				answer_text = content[s_ind + 3:]
				content = content[:s_ind - 1]
		
		return content, answer_text


	#Bonds messages
	#return object BondMessages
	async def bondingMessages(self):
		bm = BondMessages()

		last_id = self.message.author
		async for log in self.client.logs_from(self.message.channel, limit = 100, before = self.message, reverse = True):
			
			# print(log.author.name)
			# print(log.content)

			if log.author == last_id:
				bm.add(log.content)
			else:
				last_id = log.author
				bm.new(last_id)
		
		return bm


	#Create Quote Message
	async def createQuote(self, text, answer):
		self.message.content = text
		await self.quot_builder(self.message.author, answer, self.receiver, self.message)
		
		
	#Build Quote Message and send it
	#(*, Discord.message.author, str, Discord.message.author, Discord.message)
	async def quot_builder(self, author_sender, comment_text, author_receiver, text_message):

		isSelfQuote = False

		if author_sender == author_receiver:
			isSelfQuote = True
		
		print('\n')
		print('--------Founded  Message---------')
		print('author_sender: {}'.format(author_sender))
		print('isSelfQuote: {}'.format(isSelfQuote))
		print('comment_text: {}'.format(comment_text))
		print('author_receiver: {}'.format(author_receiver))
		print('text_message: {}'.format(text_message.content))
		print('text_message_date: {}'.format(text_message.timestamp))
		print('---------------------------------')
		print('\n')


		###Forming Embed message###
		
		title = ""
		#Message Text (content)
		description = text_message.content
		colour = 0xDEADBF

		author_name = author_receiver.name

		thumbnail_url = author_sender.avatar_url
		author_icon_url = author_receiver.avatar_url

		#Create Embed message
		em = discord.Embed(title = title, description = description, colour = colour)

		if isSelfQuote == False:
			if (not comment_text == None and not comment_text == ""):
				
				field_name = "Answer from " + author_sender.name
				
				#Answer text
				field_value = comment_text
					
				em.add_field(name = field_name, value = field_value)
			
			#if the comment is not exist
			else:
				field_name = "From " + author_sender.name
				em.set_footer(text = field_name)

		
		if isSelfQuote == False:
			#Sender (Quoter) Avatar
			em.set_thumbnail(url = thumbnail_url)

		#Author of quoting message (receiver)
		em.set_author(name = author_name, icon_url = author_icon_url)
		
		#Delete the command message
		await self.client.delete_message(self.message)
		
		#if there is selfquoting
		if isSelfQuote == False:
			await self.client.send_message(self.message.channel, content = "<@" + author_receiver.id + ">")

		#Send formed Embed message
		await self.client.send_message(self.message.channel, embed=em)