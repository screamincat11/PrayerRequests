class PrayerRequest:
    def __init__(self, i_reqID=None, s_title=None, d_addDate=None, d_modDate=None, s_comment=None, sar_categories=[], b_urgent=False):
        # this program can handle up to 999 requests
        self.i_reqID = i_reqID
        self.d_addDate = d_addDate
        self.d_modDate = d_modDate
        self.s_title = s_title
        self.s_comment = s_comment
        self.sar_categories = sar_categories
        self.b_urgent = b_urgent

    def getID(self):
        return self.i_reqID
    def setID(self, id):
        self.i_reqID = id

    def getDate(self):
        return self.d_modDate
    def setDate(self, newDate):
        self.d_modDate = newDate
        
    def getAddDate(self):
        return self.d_addDate
    def setAddDate(self, newDate):
        self.d_addDate = newDate

    def getTitle(self):
        return self.s_title
    def setTitle(self, title):
        self.s_title = title
        
    def getComment(self):
        return self.s_comment
    def setComment(self, comment):
        self.s_comment = comment
        
    def getCategories(self):
        return self.sar_categories
    def setCategories(self, categories):
        self.sar_categories = categories

    def getUrgent(self):
        return self.b_urgent
    def setUrgent(self, urgent):
        self.b_urgent = urgent

    def getObject(self):
        return [self.i_reqID, self.d_addDate, self.d_modDate, self.s_title, self.s_comment, self.sar_categories]

    def toString(self):
        return str(self.i_reqID).zfill(3)+"-A:"+self.d_addDate.strftime("%d %b %Y")+ "; M:"+self.d_modDate.strftime("%d %b %Y")+" "+self.s_title+" --> "+self.s_comment+" -- CATEGORIES -- "+",".join(self.sar_categories)

        
def addRequest(numlines):
    newRequest = PrayerRequest()
    newRequest.setID(numlines)
    numlines+=1
    newRequest.setTitle(input("Enter Request Title: "))
    newRequest.setAddDate(date.today())
    newRequest.setDate(date.today())
    newRequest.setComment(input("Enter Comment if Necessary: "))
    newRequest.setCategories(createCategoryArray(input("Enter Category(s), separate by \",\": ")))
    requestList.append(newRequest)
    print(newRequest.getTitle() + " has been added.\n")
    return numlines

# Helper function for addRequest that parses a string of categories into an array
def createCategoryArray(str_categories):
    #  .split(',')
    if str_categories=="":
        return []
    arr_categories = str_categories.split(',')
    return arr_categories


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
        print(wrapper.fill(request.toString()))
    print("******************************\n")

def viewRandomRequests(requestList, numlines, numrequestedreqs):
    results = []
    currentArrayLength = 0
    if numrequestedreqs > numlines:
        print("Requesting too many Requests!")
        viewRequests(requestList)
    else:
        for request in requestList:
            if request.getUrgent():
                #print("Urgent! " + str(request.getID()))
                results.append(request)
                currentArrayLength+=1
        while currentArrayLength < numrequestedreqs:
            matchFlag = 0
            randomIndex = random.randint(0,numlines-1)
            randomID = requestList[randomIndex].getID()
            for request in results:
                if request.getID() == randomID:
                    matchFlag = 1
                    break
            if matchFlag == 0:
                results.append(requestList[randomIndex])
                currentArrayLength+=1
        viewRequests(results)

            #randomRequests = random.sample(requestList, numrequestedreqs)
            #viewRequests(randomRequests)

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
        categories = ','.join(request.getCategories()).lower()
        if (mySearchTerm in title or mySearchTerm in comment or mySearchTerm in categories):
            results.append(request)
    if len(results) != 0:
        viewRequests(results)
    else:
        print("Can't find search term.")

def searchCategories(requestList, searchTerm):
    results=[]
    searchTerm=searchTerm.lower()
    for request in requestList:
        if (searchTerm in ','.join(request.getCategories()).lower()):
            results.append(request)
    if len(results) != 0:
        viewRequests(results)
    else:
        print("Can't find reqeusts with category: "+searchTerm)

def loadRequests(filename, requestList, numlines):
    # this list holds the individual lines in the file
    reqfromfile = []
    with open(filename, encoding='utf-8') as newfile:
        reqfromfile = newfile.readlines()
    
    # this loops through the lines of the file and parses out the object attributes
    for request in reqfromfile:
        newRequest = PrayerRequest()
        request=request.replace('\ufeff', '')
        # remove new line
        request=request[:-1]
        # extract date
        addday = int(request[0:2])
        addmonth = int(request[2:4])
        addyear = int(request[4:8])
        newRequest.setAddDate(date(addyear, addmonth, addday))
        day = int(request[8:10])
        month = int(request[10:12])
        year = int(request[12:16])
        newRequest.setDate(date(year, month, day))
        #print(newRequest.getAddDate())
        #print(newRequest.getDate())
        # extract request
        text=request[16:]
        title=""
        comment=""
        categories=[]
        # Get Title Loop
        j = 0
        for i in range(len(text)):
            if i < len(text)-2:
                if text[i:i+2] == "<>":
                    j=i
                    title = text[:j]
                    # make text equip comment and categories
                    text = text[j+2:]
                    # comment = text[j+2:]
                    #removes new line
                    # comment = comment[:-1]
                    break
                else:
                    continue
            else:
                print("can't find it!")
                break

        # Get Comment and Categories Loop
        j = 0
        for i in range(len(text)):
            if i < len(text)-1:
                if text[i:i+2] == "<>":
                    j=i
                    comment = text[:j]
                    str_categories = text[j+2:]
                    categories = str_categories.split(',')
                    # print(str(len(text))+text+"found it!")
                    break
                else:
                    continue
            else:
                print("strlen: "+str(len(text))+text+"can't find it!! i:"+str(i)+" sliced:"+text[i:i+2])
                break


        newRequest.setID(numlines)
        newRequest.setTitle(title)
        newRequest.setComment(comment)
        if len(comment)>=8:
            if comment[:8] == "Urgent: ":
                newRequest.setUrgent(True)
        newRequest.setCategories(categories)
        requestList.append(newRequest)
        numlines+=1
    return numlines
    
def saveFile(filename):
    with open(filename, 'w', encoding='utf-8') as newfile:
        for request in requestList:
            texttowrite = request.getAddDate().strftime("%d%m%Y") + request.getDate().strftime("%d%m%Y") + request.getTitle() + "<>" + request.getComment() + "<>" + ",".join(request.getCategories()) + "\n"
            newfile.write(texttowrite) #.encode('utf8'))
    print("*Save Successfull*\n")

def editRequest(requestList, i_reqeditnum):
    try:
        if i_reqeditnum >= 0 and i_reqeditnum < len(requestList):
            #  edit this number...


            saveflag=True
            print("Editing " + requestList[i_reqeditnum].getTitle() + "...")
            whichpart = input("Title, Comment, Category, Urgency or Mark current (t/c/a/u/m)?    (x = cancel)\n")
            whichpart = whichpart.lower()
            if whichpart=="t":
                requestList[i_reqeditnum].setTitle(input("Please enter new title: "))
                requestList[i_reqeditnum].setDate(date.today())
                print(requestList[i_reqeditnum].getTitle() + " has been updated.")
            elif whichpart=="c":
                requestList[i_reqeditnum].setComment(input("Please enter new comment: "))
                requestList[i_reqeditnum].setDate(date.today())
                print(requestList[i_reqeditnum].getTitle() + " has been updated.")
            elif whichpart=="a":
                requestList[i_reqeditnum].setCategories(createCategoryArray(input("Please enter new categories, separated by commas: ")))
                requestList[i_reqeditnum].setDate(date.today())
                print(requestList[i_reqeditnum].getTitle() + " has been updated.")
            elif whichpart=="u":
                comment = requestList[i_reqeditnum].getComment()
                if requestList[i_reqeditnum].getUrgent() == True:
                    if comment[:8]=="Urgent: ":
                        comment=comment[8:]
                        requestList[i_reqeditnum].setUrgent(False)
                        print("Urgency set to False")
                    else:
                        print("Urgency Mismatch! expected True")
                elif requestList[i_reqeditnum].getUrgent() == False:
                    if len(comment)>7:
                        if comment[:8] != "Urgent: ":
                            comment="Urgent: "+comment
                        else:
                            print("Urgency Mismatch! expected False")
                            print("comment[:8] is --" + comment[:8] + "--")
                    else:
                        # print("<=7")
                        comment="Urgent: "+comment
                    requestList[i_reqeditnum].setUrgent(True)
                    print("Urgency set to True")
                else:
                    print("Something went urgently wrong!")
                requestList[i_reqeditnum].setComment(comment)
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
    import textwrap
    os.system('cls' if os.name=='nt' else 'clear')
    saveflag = False
    boolsave = False
    requestList = []
    #categoryList = []
    numlines = 0
    numlines = loadRequests("requests.txt", requestList, numlines)
    wrapper = textwrap.TextWrapper(width=200, subsequent_indent="   ")
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
                    saveFile("requests.txt")
            print("\nGoodbye!\n")
            exit()
        elif myinput =="?": # Prints Menu
            print(menu)
        elif myinput =="": # No Input, loop again
            continue
        elif myinput =="t": # Today's Requests
            viewRandomRequests(requestList, numlines, 25)
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
        elif myinput =="c": # Search Requests for a category
            searchTerm = input("What category do you want to search for? ")
            searchCategories(requestList, searchTerm)
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
            saveFile("requests.txt")
            saveflag=False
        elif len(myinput) >= 2:
            searchRequests(requestList, myinput)
        else:
            print("* Invalid input. *\n")
