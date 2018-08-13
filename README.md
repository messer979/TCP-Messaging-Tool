# TCPy for Manhattan
A TCP Communication Tool built in Python3 specifically for Manhattan Associates End Point Testing.

Required:
  Python 3

The program is very user friendly - just follow the prompts.

Features:
Rapidly send messages to the same connection
Create and save connections

Full Manual (Available in program):

There are 4 sub programs in the "TCPy for Manhattan" tool
    
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
