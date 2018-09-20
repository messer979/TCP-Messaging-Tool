#!/usr/bin/env python

import socket, sys, ctypes
ctypes.windll.kernel32.SetConsoleTitleW("TCPy for WMOS") #changes window name
import json


def loadConfiguration(): 

    baseConfig={
        "config": {
            "Message Start": "\x02",
            "Message End": "\x03",
            "Validator": "^"
        },
        "connections": {
            "example: DEVcontainerstatus": ["localhost",
            "1521"]
        }
    }


    while True:
        try:
            with open("TCPy_cnf.json","r") as j:
                cnf = json.load(j)
                break
        except:
            print("Valid file not found. Would you like to create a new file?")
            createNew = input("y/n? ")
            if createNew.upper() == "Y":
                with open("TCPy_cnf.json","w") as j:
                    json.dump(baseConfig,j)
                with open("TCPy_cnf.json","r") as j:
                    cnf = json.load(j)
                    break
                break
            elif createNew.upper() == "N":
                "No valid connections"
                return
            else:
                print("Invalid Response")

    return cnf






################################################################################################################################################################
def addConnection():
    done = ""
    while done.upper() != "N":
        newName = input("Enter new environment and connection name: ")
                
        newHost = input("Enter hostname: ")
        while True:
            try:
                newPort = int(input("Enter port: "))
                break
            except ValueError:
                print("Please enter a number.")
                continue

        connections[newName] = [newHost,newPort]
        done = input("Add Another? \n y/n: ")

        saveJSON(confFile['config'],connections)
    return
################################################################################################################################################################

def removeConnection():

    optionsDictionary = {}
    optionsList = []

    #create menu so user can enter numbers 
    for key in connections.keys():
        optionsList.append(key)

    # keep list sorted
    optionsList = sorted(optionsList)
    
    for i in range(len(list(connections.keys()))):
        optionsDictionary[i+1] = optionsList[i]
    
    print("Type 0 when finished.")
    while True: 
        try:
            rm = int(input("Which # entry to delete? "))
        except ValueError:
            print("Please enter a number.")
            continue
        if rm == 0:
            saveJSON(confFile['config'],connections)
            break
        else:
            rmstr = optionsDictionary.get(rm)
            del connections[rmstr]
            saveJSON(confFile['config'],connections)

################################################################################################################################################################
def renameConnection():

    optionsDictionary = {}
    optionsList = []

    #create menu so user can enter numbers 
    for key in connections.keys():
        optionsList.append(key)
        
    # keep list sorted
    optionsList = sorted(optionsList)

    for i in range(len(list(connections.keys()))):
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
            return connections
        else:
            if rnstr == None:
                print("Please enter a valid number. 0 to quit.")
                continue
            newName = input("Enter new name: ")
            rninfo = connections[rnstr]
            del connections[rnstr]
            connections[newName] = rninfo
            saveJSON(confFile['config'],connections)
            print (str(newName)+ ":" + str(connections[newName]) + " is the new entry.")


################################################################################################################################################################
def viewConfig(): # THIS NEEDS WORK PRIOR TO ALLOWING USERS TO EDIT - UNABLE TO APPEND THE '\' TO A DICTIONARY ENTRY

    confFile = loadConfiguration()

    optionsDictionary = {}
    optionsList = []

    newConfig = confFile['config']
    print(newConfig)
    

    for key,val in newConfig.items():
        optionsList.append(key +": "+ repr(val))


    for i in range(len(list(newConfig.keys()))):
        optionsDictionary[i+1] = optionsList[i]

    # print("\nSelect configuration to change: ")
    print("\nCurrent Configuration")
    for num, config in sorted(optionsDictionary.items()):
        print(str(num) + ". "+config)

    input("\nTo modify this config, please edit the TCP_cnf.json file via text editor.\nEnter when finished")
    # print("Enter 0 when finished.")
    # while True: 
    #     try:
    #         cnChg = int(input("Which configuration to change? "))
    #         if cnChg == 1:
    #             newMessStart = input("Enter a new message start. Hex values should be in format 'x00':\n")
    #             newConfig["Message Start"] = newMessStart
    #         elif cnChg == 2:
    #             newMessEnd = input("Enter a new message end. Hex values should be in format 'x00':\n")
    #             newMessEnd = "\\" + newMessEnd 
    #             newConfig["Message End"] = newMessEnd.encode()
    #         elif cnChg == 3:
    #             newValidator = input("Enter a validation character (e.g. ^)\n")
    #             newConfig["Validator"] = newValidator
    #         else:
    #             break
    #     except ValueError:
    #         "Invalid Entry"
    #         continue
    # saveJSON(newConfig,confFile['connections'])



################################################################################################################################################################
def saveJSON(newConfig,newConnections):
    newJSON = {'config':newConfig, 'connections':newConnections} 
    with open("TCPy_cnf.json","w") as j:
        json.dump(newJSON,j)

################################################################################################################################################################
def SendTCP(userInput, hostname, port):
    MESSAGE = message_start + userInput + message_end
    if validator == None:
        True ==True 
    elif validator not in userInput:
        print("Probable Invalid Format\n")
        return
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, int(port)))
        s.sendto(MESSAGE.encode(),(hostname, int(port)))
        print(s.recv(2048).decode())
    
        s.close()
        print ("Success.\n")
    except ConnectionRefusedError:
        print("Connection Refused - check end point config")
    except:
        print("Unexpected error - verify connection info")

        
    



################################################################################################################################################################
def MultiLineMessage(prompt, hostname, port):
    
    
    print("Multi-Line Messaging.\n After inserting each message line, type 'f' for the final line when finished with a message.\n Type 'end' to return to single entry mode.")
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


            MESSAGE = message_start + userInput + message_end
            print(MESSAGE)                  

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
            addConnection()
            continue
        elif selection.upper() == "REMOVE" or selection.upper() == "R":
            removeConnection()
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
    print('''\nThis tool is totally written in Python. The modules used are socket, sys, ctypes, and json. Prior to this tool, the commonly used software for sending TCP messages was the TCP Test Tool. This program was lacking for several reasons. This new tool is designed specifically for Manhattan Associates use in order to simplify the job of sending TCP messages to WM. Not only are messages easier to send, but new connections to specific end points can be saved in a separate json file. This file must sit in the same folder as the "TCPy for Manhattan" program.
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
Upon logging in for the first time. Users are prompted to create a new json file in order to hold the configuration for the instance of the program. Once the file is created, users will be able to create new connections. Upon typing n or new during the first screen prompt, a user is prompted for a name, host and port. It is recommended that a connection is named based on the end point it references. Each connection is combination of a host and a port. When the connections are presented to the user, they are dynamically assigned a number in alphabetical order in order to simplify the selection process.


-Remove Connections
On the connection selection screen, a user can enter r or remove in order to remove a connection. The user simply selects the number in order to remove the entry.

-Rename Connections
On the connection selection screen, a user can enter rn or rename in order to rename a connection.

-Send Messages
Upon selecting a connection, users are presented with a prompt to send messages. Users can send messages freely to the connection. The hexcode values should not be entered with the MHE message. As this is designed specifically for Manhattan Associates use, the x02 and x03 values are automatically appended to all messages. Furthermore, a connection is opened and closed to the host each time the message is sent. Therefore, users do not need to worry about maintaining the connection.
    
    ''')
    
    # return


print("\nTCPy for WMOS")
print("Dev by CMesser")


while True:
    print("\nConfiguration file loading...")
    confFile = loadConfiguration()
    try:
        message_start = confFile['config']['Message Start']
        message_end = confFile['config']['Message End']
        validator = confFile['config']['Validator']
        connections = confFile['connections']
        break
    except:
        q = input("Error found in config file. Reset to defaults?")
        if q.upper() == 'Y' or q.upper()=='YES':
            with open("TCPy_cnf.json","w") as j:
                True
            continue
        else:
            input("Please fix manually - program will discontinue until resolved.")
            exit()
    break
print("\nType 'm' to see manual. Type 'c' to view TCPy configuration.")
selection = input("Choice: ")

if selection == 'm':
    printManual()
    input("Enter to continue")
elif selection == 'c':
    viewConfig()


    
while True:
    confFile = loadConfiguration()

    #adding config to global variables
    try:
        message_start = confFile['config']['Message Start']
        message_end = confFile['config']['Message End']
        validator = confFile['config']['Validator']
        connections = confFile['connections']
    except:
        q = input("Error found in config file. Reset to defaults?")
        if q.upper() == 'Y' or q.upper()=='YES':
            with open("TCPy_cnf.json","w") as j:
                True
            continue
        else:
            input("Please fix manually - program will discontinue until resolved.")
            exit()


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
            break
        elif prompt =='2':
            print("\nConnection Name: " + environment)
            print("Connection Detail: " + hostname + ":" + str(port))
            print("\nOptions:\n  Send messages freely. \n  Type 'm' to send a message with multiple lines. \n  Type 1 for another environment. \n  Type 2 to see environment details again.\n  Type 3 to see the manual.\n  Type 4 to quit.\n") #menu 2
        elif prompt =='3':
            printManual()
        elif prompt == '4':
            input("Thank you for using this tool.")
            exit()
        elif prompt =='m':
            MultiLineMessage(prompt,hostname,port)
            print("Returning to single line entry..")
        else:
            SendTCP(prompt, hostname, port)
