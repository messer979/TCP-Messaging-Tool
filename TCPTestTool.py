#!/usr/bin/env python

import socket, sys

def loadConnections():
    connections ={
    'example' : 	['localhost',1521],
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
    else:
        connections = pickle.load(open("TCPconnectionslist.p","rb"))
    
    return connections

################################################################################################################################################################
def addConnection():
    import pickle
    numToAdd = int(input("How many hosts would you like to add?\n"))
    for i in range(numToAdd):
        newName = input("Enter environment and connection name: ")
        newHost = input("Enter hostname: ")
        newPort = input("Enter port: ")
        savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))
        savedConnections[newName] = [newHost,newPort]
        pickle.dump(savedConnections,open("TCPconnectionslist.p","wb"))
    return savedConnections


################################################################################################################################################################
def removeConnection():
    import pickle
    savedConnections = pickle.load(open( "TCPconnectionslist.p", "rb" ))
    print("Type 0 when finished.")
    while True: 
        rm = input("Which entry to delete? ")
        if rm == '0':
            return savedConnections
        else:
            del savedConnections[rm]
            pickle.dump(savedConnections,open("TCPconnectionslist.p","wb"))

################################################################################################################################################################
    
def SendTCP(userInput, hostname, port):
    #MESSAGE ="\x02" + userInput + "\x03"
    MESSAGE = userInput
    if "^" not in userInput :
        print("Probable Invalid Format")
        print("\n")
        return
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        s.sendto(MESSAGE.encode(),(hostname, port))
        s.close()
        print ("Success.")
    except ConnectionRefusedError:
        print("Connection Refused - check end point config")



################################################################################################################################################################
def retrieveHostPort(connections):    
    
    while True:
        print("\nEnvironment options: ")
        for name in sorted(connections.keys()):
            print(name)
        print("\nnew/remove")
            
        selection = input("\nChoice: ")
        if selection == "new":
            connections = addConnection()
            continue
        elif selection == "remove":
            connections = removeConnection()
            continue
        else:
            host = connections.get(selection,"0")
            if host != "0":
                host.append(selection)
                return host
            else:
                print("Invalid Environment")
                continue
##############################################################################################################################


print("Dev2 Inventory Adjustment")

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
print(environment)
print(hostname + ":" + str(port))

print("\nOptions:\n  Send messages freely. \n  Type 1 for another environment. \n  Type 2 to see environment details again.\n  Type 3 to quit.")

while True == True:
    prompt=input("Enter Message: \n")
    if prompt == '1':
        connections = loadConnections()
        HostPort = retrieveHostPort(connections)
        hostname = HostPort[0]
        port = HostPort[1]
        environment = HostPort[2]
        print(environment)
        print(hostname + ":" + str(port))
        print("\nOptions:\n  Send messages freely. \n  Type 1 for another environment. \n  Type 2 to see environment details again.\n  Type 3 to quit.")
    elif prompt =='2':
        print(environment)
        print(hostname + ":" + str(port))
        print("\nOptions:\n  Send messages freely. \n  Type 1 for another environment. \n  Type 2 to quit.\n")
    elif prompt =='3':
        break
    else:
        SendTCP(prompt, hostname, port)
