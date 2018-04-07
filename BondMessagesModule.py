'''
!!!FIX: change the Cortege to List

		bond_messages
		List:		cortege
			0. (user1, string1)
			1. (user2, string1)
			2. (user1, string2)
			3. (user2, string2)
			4. (user1, string3)
			
'''

class BondMessages:

	bond_messages 	= []
	#bond 			= (user, string)


	def __init__(self):
		pass
	

	#retutn <bond_messages>
	def getBondMessages(self):
		return self.bond_messages


	#add <line> to string in last element of List
	def add(self, line):
		try:
			self.bond_messages[-1] = tuple([self.bond_messages[-1][0], self.bond_messages[-1][1] + line + '\n'])
		except:
			# fix this
			print("------------------Out from range------------------")
			print("line:", line)
	

	#create new element in List with <user>
	def new(self, user):
		self.bond_messages.append(tuple([user, ""]))


	#small test show
	def show(self):
		for bond in self.bond_messages:
			print(bond[0])
			print(bond[1])

	
	#find <quote> in <bond_messages>
	#return (string, user) or (None, None)
	def findTheQuote(self, quote):
		for bond in reversed(self.bond_messages):
			if quote in bond[1]:	
				return self.razoredQuote(bond[1], quote), bond[0]

		return None, None


	#Find lines with quot and glue its to whole single text
	def razoredQuote(self, text, quote):
		#Finding start index
		start_ind = text.rfind('\n', 0, text.rfind(quote)) + 1
		#Finding end index
		end_ind = text.find('\n', text.rfind(quote) + len(quote))

		result_quote = text[start_ind:end_ind]

		return result_quote

