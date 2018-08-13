#!/usr/bin/env python

import socket, sys, ctypes
ctypes.windll.kernel32.SetConsoleTitleW("Manhattan TCPy") #changes window name


def loadConnections():
    connections ={
    
    "example:'DEV containerstatus'" : 	['localhost',1521],
    }

    import pickle
    while True:
        try:
            savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))
            break
        except FileNotFoundError:
            print("No prior connections found. Would you like to create a new file?")
            createNew = input("y/n? ")
            if createNew.upper() == "Y":
                savedConnections = "create"
                break
            elif createNew.upper() == "N":
                "No valid connections"
                return
            else:
                print("Invalid Response")

        
    if savedConnections == "create":
        pickle.dump(connections,open("TCPconnectionslist.p","wb"))
        connections = pickle.load(open("TCPconnectionslist.p","rb"))
    else:
        connections = pickle.load(open("TCPconnectionslist.p","rb"))
    
    return connections

################################################################################################################################################################
def addConnection():
    import pickle
    done = ""
    while done.upper() != "N":
        newName = input("Enter new environment and connection name: ")
            # I think this isn't necessary since users must select a number option which is dynamically assigned.
            # if newName.upper == "N" or newName.upper == "R" or newName.upper == "NEW" or newName.upper == "REMOVE": 
                # print("Name not allowed")
                # continue
                
        newHost = input("Enter hostname: ")
        while True:
            try:
                newPort = int(input("Enter port: "))
                break
            except ValueError:
                print("Please enter a number.")
                continue
        savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))
        savedConnections[newName] = [newHost,newPort]
        pickle.dump(savedConnections,open("TCPconnectionslist.p","wb"))
        done = input("Add Another? \n y/n: ")
    return savedConnections

################################################################################################################################################################

def removeConnection():
    import pickle
    savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))

    optionsDictionary = {}
    optionsList = []

    #create menu so user can enter numbers 
    for key in savedConnections.keys():
        optionsList.append(key)

    # keep list sorted
    optionsList = sorted(optionsList)
    
    for i in range(len(list(savedConnections.keys()))):
        optionsDictionary[i+1] = optionsList[i]
    
    print("Type 0 when finished.")
    while True: 
        try:
            rm = int(input("Which # entry to delete? "))
        except ValueError:
            print("Please enter a number.")
            continue
        if rm == 0:
            return savedConnections
        else:
            rmstr = optionsDictionary.get(rm)
            del savedConnections[rmstr]
            pickle.dump(savedConnections,open("TCPconnectionslist.p","wb"))

################################################################################################################################################################
def renameConnection():

    import pickle
    savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))

    optionsDictionary = {}
    optionsList = []

    #create menu so user can enter numbers 
    for key in savedConnections.keys():
        optionsList.append(key)
        
    # keep list sorted
    optionsList = sorted(optionsList)

    for i in range(len(list(savedConnections.keys()))):
        optionsDictionary[i+1] = optionsList[i]
    
    print("Type 0 when finished.")
    while True: 
        try:
            rn = int(input("Which # entry to rename? "))
            rnstr = optionsDictionary.get(rn)
        except (ValueError) as e:
            print("Please enter a valid number. 0 to quit.")
            continue
        if rn == 0:
            return savedConnections
        else:
            if rnstr == None:
                print("Please enter a valid number. 0 to quit.")
                continue
            newName = input("Enter new name: ")
            rninfo = savedConnections[rnstr]
            del savedConnections[rnstr]
            savedConnections[newName] = rninfo
            pickle.dump(savedConnections,open("TCPconnectionslist.p","wb"))
            print (str(newName)+ ":" + str(savedConnections[newName]) + " is the new entry.")



################################################################################################################################################################
def SendTCP(userInput, hostname, port):
    MESSAGE ="\x02" + userInput + "\x03"
    if "^" not in userInput :
        print("Probable Invalid Format\n")
        return
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendto(MESSAGE.encode(),(hostname, port))
        s.close()
        print ("Success.\n")
    except ConnectionRefusedError:
        print("Connection Refused - check end point config")
        
    



################################################################################################################################################################
def MultiLineMessage(prompt, hostname, port):
    
    
    print("Multi-Line Messaging. Input 'f' when finished with a message.\nType 'end' to return to single entry mode.")
    while prompt != 'end':
        promptList = []
        lineCounter = 1
        prompt = input("Enter each line one at a time.\nLine {}: ".format(lineCounter))
        if prompt == 'end':
            break
        else:
            while prompt != 'f':
                promptList.append(prompt)
                lineCounter += 1
                prompt = input("Line {}: ".format(lineCounter))
                continue

            userInput = '\n'.join(promptList)


            MESSAGE ="\x02" + userInput + "\x03" ##testing
            print(MESSAGE)                ##testing            

            SendTCP(userInput, hostname, port)
            continue
    return

################################################################################################################################################################
def retrieveHostPort(connections):    #obtains the specific host from the dictionary 

    while True:
        optionsDictionary = {}
        optionsList = []

        #create menu so user can enter number
        for key in connections.keys():
            optionsList.append(key)
        
        #sort list to present in alphabetical order
        optionsList = sorted(optionsList)
        
        for i in range(len(list(connections.keys()))):
            optionsDictionary[i+1] = optionsList[i]

        print("\nSelect Environment: ")
        for name, env in sorted(optionsDictionary.items()):
            print(str(name) + ". "+env)
        print("\nnew/remove/rename")

        selection = input("\nChoice: ")
        if selection.upper() == "NEW" or selection.upper() == "N":
            connections = addConnection()
            continue
        elif selection.upper() == "REMOVE" or selection.upper() == "R":
            connections = removeConnection()
            continue
        elif selection.upper() == "RENAME" or selection.upper() == "RN":
            connections = renameConnection()
        else:
            try:
                indexSelection = optionsDictionary.get(int(selection),"0")
            except ValueError:
                print("Invalid Selection - try again.")
                continue
            host = connections.get(indexSelection,"0")
            if host != "0":
                host.append(indexSelection)
                return host
            else:
                print("Invalid Environment")
                continue
##############################################################################################################################

def printManual():
    

#    left padding 20, right padding 20
    print('\nThank you for using the TCPy Test Tool for Manhattan'.center(100,'*')) 
    print('If you have questions please feel free to email them directly to cmesser@manh.com'.center(100,'*'))
    
    
    print('\nDescription of Tool and Purpose')
    print('''\nThis tool is totally written in Python. The modules used are socket, sys, ctypes, and pickle. Prior to this tool, the commonly used software for sending TCP messages was the TCP Test Tool. This program was lacking for several reasons. This new tool is designed specifically for Manhattan Associates use in order to simplify the job of sending TCP messages to WM. Not only are messages easier to send, but new connections to specific end points can be saved in a separate 'pickle' file. This file is not editable apart from this program and must sit in the same folder as the "TCPy for Manhattan" program.
    ''')
    
    print('\nGeneral Usage')
    print('''There are 4 sub programs in the "TCPy for Manhattan" tool
    
   *Add Connections
   *Remove Connections
   *Rename Connections
   *Send messages
   *Send multi-line message
   \n
-Add Connections 
Upon logging in for the first time. Users are prompted to create a new pickle file in order to create a persistent dictionary of all connections. Once the pickle file is created, users will be able to create new connections. Upon typing n or new during the first screen prompt, a user is prompted for a name, host and port. It is recommended that a connection is named based on the end point it references. Each connection is combination of a host and a port. When the connections are presented to the user, they are dynamically assigned a number in alphabetical order in order to simplify the selection process.


-Remove Connections
On the connection selection screen, a user can enter r or remove in order to remove a connection. The user simply selects the number in order to remove the entry.

-Rename Connections
On the connection selection screen, a user can enter rn or rename in order to rename a connection.

-Send Messages
Upon selecting a connection, users are presented with a prompt to send messages. Users can send messages freely to the connection. The hexcode values should not be entered with the MHE message. As this is designed specifically for Manhattan Associates use, the x02 and x03 values are automatically appended to all messages. Furthermore, a connection is opened and closed to the host each time the message is sent. Therefore, users do not need to worry about maintaining the connection.
    
    ''')
    
    # return


print("TCP Messaging Tool")
print("Dev by CMesser")

print("\nType 'm' to see manual. Else hit enter to start program.")
selection = input("Choice: ")

if selection == 'm':
    printManual()
    input("Enter to continue")

    
    



connections = loadConnections()

HostPort = retrieveHostPort(connections)    

if HostPort == None:
    print("Failed to get connection info.")
    print ("Try again?")
    response = input("y/n?")
    if response.upper() == 'Y':
        HostPort = retrieveHostPort(connections)
    else:
        sys.exit()

hostname = HostPort[0]
port = HostPort[1]
environment = HostPort[2]
print("\nConnection Name: " + environment)
print("Connection Detail: " + hostname + ":" + str(port))

    
print("\nOptions:\n  Send messages freely. \n  Type 'm' to send a message with multiple lines. \n  Type 1 for another environment. \n  Type 2 to see environment details again.\n  Type 3 to see the manual.\n  Type 4 to quit.\n") #menu 2

while True:
    prompt=input("Enter Message: \n")
    if prompt == '1':
        connections = loadConnections()
        HostPort = retrieveHostPort(connections)
        hostname = HostPort[0]
        port = HostPort[1]
        environment = HostPort[2]
        print("\nConnection Name: " + environment)
        print("Connection Detail: " + hostname + ":" + str(port))
    elif prompt =='2':
        print("\nConnection Name: " + environment)
        print("Connection Detail: " + hostname + ":" + str(port))
    elif prompt =='3':
        printManual()
    elif prompt == '4':
        input("Thank you for using this tool.")
        break
    elif prompt =='m':
        MultiLineMessage(prompt,hostname,port)
        print("Returning to single line entry..")
    else:
        SendTCP(prompt, hostname, port)
