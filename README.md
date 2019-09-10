# TCPy for Manhattan WMOS
A TCP Communication Tool built in Python3 specifically for Manhattan Associates MHE messaging.

The program is very user friendly - just follow the prompts.

**If you do not want to install python - simply download the TCPy for WMOS.exe file.**

## Features:
- Rapidly send messages to the same connection
- View past messages sent in command line
- Create and save connections
- Specify option to send several lines in a single message

## Full Manual (Available in program):
This tool is totally written in Python. The modules used are socket, sys, ctypes, and pickle. Prior to this tool, the commonly used software for sending TCP messages was the TCP Test Tool. This program was lacking for several reasons. This new tool is designed specifically for Manhattan Associates use in order to simplify the job of sending TCP messages to WM. Not only are messages easier to send, but new connections to specific end points can be saved in a separate 'pickle' file. This file is not editable apart from this program and must sit in the same folder as the "TCPy for WMOS" program.

There are 5 sub programs in the "TCPy for WMOS" tool
    
 1. Add Connections
 2. Remove Connections
 3. Rename Connections
 4. Send messages
 5. Send multi-line message
 
- Add Connections 
  - Upon logging in for the first time. Users are prompted to create a new pickle file in order to create a persistent dictionary of all connections. Once the pickle file is created, users will be able to create new connections. Upon typing n or new during the first screen prompt, a user is prompted for a name, host and port. It is recommended that a connection is named based on the end point it references. Each connection is combination of a host and a port. When the connections are presented to the user, they are dynamically assigned a number in alphabetical order in order to simplify the selection process.


- Remove Connections
  - On the connection selection screen, a user can enter r or remove in order to remove a connection. The user simply selects the number in order to remove the entry.

- Rename Connections
  - On the connection selection screen, a user can enter rn or rename in order to rename a connection.

- Send Messages
  - Upon selecting a connection, users are presented with a prompt to send messages. Users can send messages freely to the connection. The hexcode values should not be entered with the MHE message. As this is designed specifically for Manhattan Associates use, the x02 and x03 values are automatically appended to all messages. Furthermore, a connection is opened and closed to the host each time the message is sent. Therefore, users do not need to worry about maintaining the connection. 

  - A validation exists to verify the message has at least one '^' character within it in order to prevent the accidental sending of data. If a client has an MHE format which excludes the '^', this validation must be removed from the code manually. 

- Send multi-line messages
  - After the send message prompt is displayed, users may enter 'm' in order to send a multi-line message. Each line from the message is entered one at a time. (You can copy however many lines you want and paste them simultaneously to do this rapidly.) The message is then compiled so that each line is separated by a return (\n) and the message is sent with the hex values.
