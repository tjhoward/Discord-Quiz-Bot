import discord #discord.py library
#import os             
#from replit import db



client = discord.Client() #create client instance to discord

class quiz(discord.Client):
	def __init__(self, user_name):
		self.user_name = user_name
		#self.quizzes = [["1$quizname", "Question ***", "Answer *** "], ["2$quizname", "Question ***", "Answer **"]] #list will have quesitons, answers, and name, so mult by 2 and 1 to length *((numQuestions*2) + 1
		self.quizzes = []
		self.new_quiz_questions = [] #used to store questions that are being created
		self.quizCount = 0
		self.has_quiz = False
		self.creating_questions = False
		self.creating_index = 0
		self.creating_qnum = 0
		self.takingQuiz = False
		self.choosingQuiz = False
		self.current_quiz = 0 # the quiz user is currently taking
		self.current_quiz_quest = 0 #used to 
		self.quizing_index = 0 #used to loop through quiz quesitons


	def getName(self):
		return self.user_name

	def settName(self, new_name):
		self.user_name = new_name

	def printQuiz(self):

		count = 1
		q = self.quizzes
		#print(q)
		if len(q) > 0:
			for i in range(len(q)):
				print(q[i][0])

				if q[i][0].find(str(count) + "$")  != -1:   #count occurences in form quiznum$
					#print("found")
					print(q[i][0].replace("$", ". "))
					count += 1
			return True
		else:
			return False
	




@client.event #Notify when bot is ready
async def on_ready():
	print('Bot {0.user}'.format(client) + 'is ready')
	#if Permissions(read_message_history,client.user) == TRUE:
	print("Success logging in")



users = []
q = quiz("") # store username and quiz questions


@client.event
async def on_message(message): #Called whenever a message is sent on a channel

	if message.author == client.user: #ignore if message is from bot
		return

	currentQuizTaker = q.user_name
	#print("CURRENT QUIZ TAKER " + q.user_name)

	m = message.content #get message
	m_auth = message.author # the Member that sent the message
	a = str(m_auth)
	name_split = a.split("#")
	name = name_split[0]
	prev_message = ""




	counter = 0
	async for message in message.channel.history(limit=3): #get the PREVIOUS message of the user
		#print(message.content)
		if message.author == m_auth and prev_message == "" and counter >= 1:
			prev_message = message.content
		counter += 1


	if m.startswith('$greeting'): #have bot say hello
		await message.channel.send('Hello!')

	if m.startswith('$quiz') and currentQuizTaker == "": #user initiates quiz bot

		print("entered45")
		#TODO check if they a quiz session is already active
		#     check if user has a quiz in database and create a quiz object with that info if so
		
		q.user_name = a
		await message.channel.send('Hello ' + name + ', it\'s Quiz Time! Do you want to start a quiz, or create one? Type: $create or $start')

	elif currentQuizTaker == a and (prev_message == "$quiz" or q.creating_questions == False) and q.choosingQuiz == False and q.takingQuiz == False:

		print("entered78")
		if m.startswith('$create'):
			await message.channel.send('What should the name of the quiz be? Type: $<quiz name>')
			q.creating_questions = True

		if m.startswith('$start'):

			if q.printQuiz() == True:	#if has quizzes on file, print out a list
				q.has_quiz = True
				count  = 1
				output = ""
				for i in range(len(q.quizzes)):
					#print(q.quizzes[i][0] + "FOUND-")

					if q.quizzes[i][0].find(str(count) + "$")  != -1:   #count occurences in form quiznum$
						#print("found")
						#print(q[i][0].replace("$", ". "))
						output = output + q.quizzes[i][0].replace("$", ". ") + " "
						count += 1

				await message.channel.send(output)
				await message.channel.send("Here are a list of your quizzes.\nEnter $ <quiz number> to choose one ")
				q.choosingQuiz = True

			else:
				await message.channel.send("You do not have any quizzes!!!!")


	elif currentQuizTaker == a and (prev_message == "$create" or q.creating_questions == True) and q.takingQuiz == False:  #where user can create questions,    ###BUG, FIX CONDITIONALS 

		print("entered")
		if q.creating_index == 0:
			q.new_quiz_questions.clear()
			q.quizCount += 1
			q.new_quiz_questions.append(str(q.quizCount) + "$" + m)
			q.creating_index += 1


		if m.startswith("$X") and q.creating_index == 2: # stop entering questions
			await message.channel.send("Quiz Saved!! Use $start command to start quiz!")
			q.quizCount += 1
			q.creating_questions = False
			q.creating_index = 0
			q.quizzes.append(q.new_quiz_questions)

		if q.creating_index == 1:  # go back and forth with asking questions / getting answers until done

			await message.channel.send("Enter a Question or enter $X if done ")
			q.creating_index = 2


		elif q.creating_index == 2:

			q.new_quiz_questions.append("Question: " + m)
			await message.channel.send("Enter the answer to the Question ")
			q.creating_index = 3

		elif q.creating_index == 3:

			q.new_quiz_questions.append("ANSWER: " + m)
			q.creating_index = 2
			await message.channel.send("Enter a Question or enter $X if done ")
			


				#TODO add method in quiz object that checks that parses $num and checks if there is a quiz with that number
	elif currentQuizTaker == a and m.startswith("$") and q.has_quiz == True and q.creating_questions == False and q.choosingQuiz == True:  # When user is choosing the questions

		#print("entered24")

		try:
			s = m.split("$")
			q.current_quiz = int(s[1])
			await message.channel.send("Starting Quiz")
			await message.channel.send(q.quizzes[int(q.current_quiz) - 1][q.current_quiz_quest + 1])
			q.takingQuiz = True
			q.choosingQuiz = False
		except:
			await message.channel.send("Invalid Quiz Number. Enter choice as $<quiz number>")



	elif currentQuizTaker == a and  q.has_quiz == True and q.creating_questions == False and q.takingQuiz == True: #when user is answering the question

		print("Quiz" + str(q.current_quiz) + "chosen")


		questions = len(q.quizzes[int(q.current_quiz) - 1]) - 1   # minus one since we show list starting at 1 and also since index 0 is for name only

		if questions != q.current_quiz_quest:

			if q.quizing_index == 0:
				q.current_quiz_quest = 0
				await message.channel.send(q.quizzes[int(q.current_quiz) - 1][q.current_quiz_quest+ 2] )  # first answer
				await message.channel.send( "Enter $next to continue")
				q.current_quiz_quest += 2
				q.quizing_index = 1

			elif q.quizing_index == 1:
				await message.channel.send(q.quizzes[int(q.current_quiz) - 1][q.current_quiz_quest + 1]) #question
				q.quizing_index = 2

			elif q.quizing_index == 2:
				await message.channel.send(q.quizzes[int(q.current_quiz) - 1][q.current_quiz_quest + 2]) #answer
				await message.channel.send( "Enter $next to continue")
				q.quizing_index = 1
				q.current_quiz_quest += 2
			
	
		else:
			await message.channel.send("Finished Quiz!!")
			await message.channel.send("Good Job!!")
			q.takingQuiz = False
			q.new_quiz_questions.clear()
			q.creating_index = 0
			q.current_quiz = 0
			q.current_quiz_quest = 0





	#DEBUG--
	#msg = await message.channel.history(limit = 5).get(author__name= name) #get the last message from user
	#print(msg.content)
	#print("PREVIOUS MESSAGE " + prev_message)
	#print("create index " + str(q.creating_index))


#Enter the bots key here. I removed mine here as it should not be public :)
client.run("key") #run bot


#discord.py docs https://discordpy.readthedocs.io/en/latest/api.html#discord.Message.author

