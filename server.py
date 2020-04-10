'''
Multiuser chat with sockets in Python

Developed by Alessio Rubicini

Python 3.6.9 - 64 bit


SERVER SIDE

'''

# ================= Modules ======================

import socket as sock       # Comunicazione in rete
import threading as th      # Gestione thread


# ================= Variables ======================

utenti = []         # List of connected users



# ================= Functions ======================


# Create a thread to manage the client
# Parameters: connection descriptor, client address
def client_thread(conn, address):

    # Send a welcome message
    benvenuto = "Welcome to the chat!".encode()
    conn.send(benvenuto)

    while True:

        # Try to receive a message from a client
        try:
            
            message = conn.recv(4096)

            # If the message is not empty
            if message:

                if message == "CLOSE":
                    server.close()
                    exit()
                
                # Forward the message to all the other users
                broadcast(message, conn)

                print(message)

            # If the message is empty the connection may be broken so it removes it
            else:

                utenti.remove(conn)

        except:
            continue

# Broadcast a message to all the other users
def broadcast(message, connection):

    for utente in utenti:
        
        # Check if the user is not the one who sent the message
        if utente != connection:
            
            # Try to forward the message
            try:
                utente.send(message)

            # If the connection fails it may be broken then remove it
            except:
                utente.close()

                utenti.remove(utente)



# ================= Execution ======================

# Takes as input IP address and port on which to host the server
host_ip = str(input("Indirizzo IP host: "))
host_port = int(input("Porta host: "))

# Socket creation
server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# Bind to address and port
server.bind((host_ip, host_port))

print("Server listening on {I}:{P}....".format(I=host_ip, P=host_port))

# Server listening for clients...
server.listen(10)

while True:

    # Accept client connection
    conn, addr = server.accept()

    # Add the user to the connected user list
    utenti.append(conn)

    print("Connessione stabilita con: ", addr)

    # Create a new thread for the client
    th._start_new_thread(client_thread, (conn, addr))



conn.close()
server.close()

