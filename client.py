'''
Multiuser chat with sockets in Python

Developed by Alessio Rubicini

Python 3.6.9 - 64 bit


CLIENT SIDE

'''

# ================= Modules ======================

from tkinter import *       # GUI
import socket as sock       # Socket
import select               # I/O management
import sys                  # System's functions


# ================= Execution ======================

# Input of server IP address, server port and username
server_ip = str(input("Indirizzo IP chat: "))
server_port = int(input("Porta chat: "))
username = str(input("Il tuo username: "))

# Socket creation
server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Connection to the server
server.connect((server_ip, server_port))


while True:

    # List of possible input streams
    sockets_list = [sys.stdin, server]

    # Wait until one of the specified descriptors is ready for I/O
    read, write, error = select.select(sockets_list, [], [])

    for socks in read:

        # Receive message from another user
        if socks == server:
            message = socks.recv(2048)
            message = message.decode("utf-8")
            
            try:
                message = message.split(";")
                # Message[0]: sender's username
                # Message[1]: message content
                print(message[0] + ": " + message[1])
            except:
                continue

        else:
            # Send a message to other users
            message = sys.stdin.readline()
            message = username + ";" + message
            server.send(message.encode())
            print("You: ", message)



server.close()


