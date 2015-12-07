class PrayerRequest:
	def __init__(self, i_reqID=None, s_title=None, d_modDate=None, s_comment=None):
		# this program can handle up to 999 requests
		self.i_reqID = i_reqID
		self.d_modDate = d_modDate
		self.s_title = s_title
		self.s_comment = s_comment

	def getID(self):
		return self.i_reqID
	def setID(self, id):
		self.i_reqID = id

	def getDate(self):
		return self.d_modDate
	def setDate(self, newDate):
		self.d_modDate = newDate
		
	def getTitle(self):
		return self.s_title
	def setTitle(self, title):
		self.s_title = title
		
	def getComment(self):
		return self.s_comment
	def setComment(self, comment):
		self.s_comment = comment
		
	def getObject(self):
		return [self.i_reqID, self.d_modDate, self.s_title, self.s_comment]

	def toString(self):
		return str(self.i_reqID).zfill(3)+"-"+self.d_modDate.strftime("%d %b %Y")+" "+self.s_title+" --> "+self.s_comment

		
def addRequest(numlines):
	newRequest = PrayerRequest()
	newRequest.setID(numlines)
	numlines+=1
	newRequest.setTitle(input("Enter Request Title: "))
	newRequest.setDate(date.today())
	newRequest.setComment(input("Enter Comment if Necessary: "))
	requestList.append(newRequest)
	print(newRequest.getTitle() + " has been added.\n")
	return numlines

def delRequest(numlines):
	while True:
		reqdeletenum = input("Which request do you want to delete? ")
		try:
			index = int(reqdeletenum)
			if index >= 0 and index < len(requestList):
				break
			else:
				print("* Please type an integer from 0 to " + str(len(requestList)-1)+" *\n")
				continue
		except (TypeError, ValueError):
			print("* Please type an integer from 0 to " + str(len(requestList)-1)+" *\n")
	title=requestList[int(index)].getTitle()
	choice = input("Are you sure you want to delete "+title+"? [y/n] ")
	choice = choice.lower()
	if choice == "y":
		requestList[int(index):int(index)+1]=[]
		numlines-=1
		renumber()
		print(title+" has been deleted.\n")
	else:
		print(title+" has not been deleted.\n")
	return numlines

def renumber():
	for i in range(len(requestList)):
		requestList[i].setID(i)
			
def viewRequests(requestList):
	print("\n******************************")
	print("Request List")
	print("------------------------------")
	for request in requestList:
		print(request.toString())
	print("******************************\n")

def viewRandomRequests(requestList):
	randomRequests = random.sample(requestList, 25)
	viewRequests(randomRequests)

def viewOldRequests(requestList):
    oldRequests=[]
    for request in requestList:
        timeDelta = date.today() - request.d_modDate
        if timeDelta.days > 120:
            oldRequests.append(request)
    if len(oldRequests) != 0:
        oldRequests.sort(key=lambda request: request.d_modDate)
        if len(oldRequests) > 10:
            del oldRequests[10:]
        viewRequests(oldRequests)
    else:
        print("All requests are up to date.")

def searchRequests(requestList, searchTerm):
    results=[]
    mySearchTerm = searchTerm.lower()
    for request in requestList:
        title = request.getTitle().lower()
        comment = request.getComment().lower()
        if (mySearchTerm in title or mySearchTerm in comment):
            results.append(request)
    if len(results) != 0:
        viewRequests(results)
    else:
        print("Can't find search term.")

def loadRequests(filename, requestList, numlines):
	# this list holds the individual lines in the file
	reqfromfile = []
	with open(filename) as newfile:
		reqfromfile = newfile.readlines()
	
	# this loops through the lines of the file and parses out the object attributes
	for request in reqfromfile:
		newRequest = PrayerRequest()
		# extract date
		day = int(request[0:2])
		month = int(request[2:4])
		year = int(request[4:8])
		newRequest.setDate(date(year, month, day))
		# extract request
		text=request[8:]
		title=""
		comment=""
		j = 0
		for i in range(len(text)):
			if i < len(text)-2:
				if text[i:i+2] == "<>":
					j=i
					title = text[:j]
					comment = text[j+2:]
					#removes new line
					comment = comment[:-1]
					break
				else:
					continue
			else:
				print("can't find it!")
				break
		newRequest.setID(numlines)
		newRequest.setTitle(title)
		newRequest.setComment(comment)
		requestList.append(newRequest)
		numlines+=1
	return numlines
	
def saveFile(filename):
	with open(filename, 'w') as newfile:
		for request in requestList:
			newfile.write(request.getDate().strftime("%d%m%Y") + request.getTitle() + "<>" + request.getComment() + "\n")
	print("*Save Successfull*\n")

def editRequest(requestList, i_reqeditnum):
	try:
		if i_reqeditnum >= 0 and i_reqeditnum < len(requestList):
			#  edit this number...


			saveflag=True
			print("Editing " + requestList[i_reqeditnum].getTitle() + "...")
			whichpart = input("Title, Comment, or Mark current (t/c/m)?    (x = cancel)\n")
			whichpart = whichpart.lower()
			if whichpart=="t":
				requestList[i_reqeditnum].setTitle(input("Please enter new title: "))
				requestList[i_reqeditnum].setDate(date.today())
				print(requestList[i_reqeditnum].getTitle() + " has been updated.")
			elif whichpart=="c":
				requestList[i_reqeditnum].setComment(input("Please enter new comment: "))
				requestList[i_reqeditnum].setDate(date.today())
				print(requestList[i_reqeditnum].getTitle() + " has been updated.")
			elif whichpart=="m":
				requestList[i_reqeditnum].setDate(date.today())
				print(requestList[i_reqeditnum].getTitle() + " has been updated.")
			elif whichpart=="x":
				saveflag=False
			else:
				print("* Invalid input. *\n")

		else:
			pass
	except (TypeError, ValueError):
		pass
	return saveflag


	
		
if __name__ == "__main__":
	import sys
	from datetime import date
	import random
	import os
	os.system('cls' if os.name=='nt' else 'clear')
	saveflag = False
	boolsave = False
	requestList = []
	#categoryList = []
	numlines = 0
	numlines = loadRequests("requests", requestList, numlines)
	menu = "Pick an action:\nt. Today's Requests\no. View Old Requests\nv. View All Requests\na. Add New Request\nf. Find Request\ne. Edit Request\nd. Delete Request\ns. Save\nq. Quit\n?  Show Menu\n"

	print("*************************************************************")
	print("*          Welcome to the Prayer Request Organizer          *")
	print("*************************************************************")
	print(menu)
		
	while True:
		myinput = input("> ")
		myinput = myinput.lower()
		try:
			i_reqeditnum = int(myinput)
			if i_reqeditnum >= 0 and i_reqeditnum < len(requestList):
				boolsave = editRequest(requestList, i_reqeditnum)
				saveflag = saveflag or boolsave
				continue
			else:
				continue
		except (TypeError, ValueError):
			pass


		if myinput =="q": # Quit
			if saveflag:
				yesno = input("Do you want to save (y/n)? ")
				yesno=yesno.lower()
				if yesno=="y":
					saveFile("requests")
			print("\nGoodbye!\n")
			exit()
		elif myinput =="?": # Prints Menu
			print(menu)
		elif myinput =="": # No Input, loop again
			continue
		elif myinput =="t": # Today's Requests
			viewRandomRequests(requestList)
		elif myinput =="o": # Old Requests
			viewOldRequests(requestList)
		elif myinput =="v": # View All Requests
			viewRequests(requestList)
		elif myinput =="a": # Add New Request
			numlines=addRequest(numlines)
			saveflag=True
		elif myinput =="f": # Search Requests
			searchTerm = input("What do you want to search for? ")
			searchRequests(requestList, searchTerm)
		elif myinput =="e": # Edit Request
			while True:
				reqeditnum = input("Which request do you want to edit? ")
				try:
					i_reqeditnum = int(reqeditnum)
					if i_reqeditnum >= 0 and i_reqeditnum < len(requestList):
						break
					else:
						print("* Please type an integer from 0 to " + str(len(requestList)-1)+" *\n")
						continue
				except (TypeError, ValueError):
					print("* Please type an integer from 0 to " + str(len(requestList)-1)+" *\n")
			boolsave = editRequest(requestList, i_reqeditnum)
			saveflag = saveflag or boolsave
		elif myinput =="d": # Delete Request
			numlines=delRequest(numlines)
			saveflag=True
		elif myinput =="s": # Save
			saveFile("requests")
			saveflag=False
		elif len(myinput) >= 2:
			searchRequests(requestList, myinput)
		else:
			print("* Invalid input. *\n")
