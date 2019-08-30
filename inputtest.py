def loadRequests(filename, requestList, numlines):
    # this list holds the individual lines in the file
    reqfromfile = []
    print("function call: loadRequests")
    with open(filename, encoding='utf-8') as newfile:
        newfile.read()
        reqfromfile = newfile.readlines()
    
    # this loops through the lines of the file and parses out the object attributes
    for request in reqfromfile:
        request=request.replace('\ufeff', '')
        # remove new line
        request=request[:-1]
        # adds line from file into array
        requestList.append(request)
        numlines+=1
    return numlines
    
def saveFile(filename):
    with open(filename, 'w') as newfile:
        for request in requestList:
            newfile.write(request.getAddDate().strftime("%d%m%Y") + request.getDate().strftime("%d%m%Y") + request.getTitle() + "<>" + request.getComment() + "<>" + ",".join(request.getCategories()) + "\n")
    print("*Save Successfull*\n")

def viewRequests(requestList):
    print("\n******************************")
    print("Request List")
    print("------------------------------")
    for request in requestList:
        print(request)
    print("******************************\n")
        
if __name__ == "__main__":
    import sys
    from datetime import date
    import random
    import os
    # os.system('cls' if os.name=='nt' else 'clear')
    saveflag = False
    boolsave = False
    requestList = []
    #categoryList = []
    # so I only have to change file name in one place
    savefile = "inputtest.txt"
    numlines = 0
    with open(savefile, encoding='utf-8') as newfile:
        contents = newfile.read()
        print(contents)
    # numlines = loadRequests(savefile, requestList, numlines)
    # menu = "Pick an action:\nt. Today's Requests\no. View Old Requests\nv. View All Requests\na. Add New Request\nf. Find Request\ne. Edit Request\nd. Delete Request\ns. Save\nq. Quit\n?  Show Menu\n"

    # print("*************************************************************")
    # print("*          Welcome to the Prayer Request Organizer          *")
    # print("*************************************************************")
    # print(menu)
        
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
                    saveFile(savefile)
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
            saveFile(savefile)
            saveflag=False
        elif len(myinput) >= 2:
            searchRequests(requestList, myinput)
        else:
            print("* Invalid input. *\n")
