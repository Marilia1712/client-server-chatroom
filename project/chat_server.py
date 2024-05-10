from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


#broadcast function to send a message to all the users in the chatroom.
def broadcast(msg, prefix=""):
    for user in clients:
        user.send(bytes(prefix, ENCODING)+msg)

def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s joined the chatroom." %client_address)
        #info for first-time clients
        client.send(bytes("Welcome! Insert your name and press Shift+E", ENCODING))
        addresses[client] = client_address
        #starting the thread
        Thread(target=manage_client, args=(client,)).start()
        if len(addresses) == 1 :
            client.send(bytes("The chatroom is empty... You're the first one to join.", ENCODING))


def manage_client(client):
    name = client.recv(BUFSIZE).decode(ENCODING)
    #welcome and info on how to quit
    welcome = 'Welcome %s! If you want to leave the chatroom, you can press Shift+Q' %name 
    client.send(bytes(welcome,ENCODING))
    #message to inform all clients about the new join
    msg = "%s joined the chat" %name
    broadcast(bytes(msg, ENCODING))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZE)
        if msg != bytes("Q", ENCODING):
            broadcast(msg, name+": ")
        #the client wants to quit the chatroom
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chatroom." % name, ENCODING))
            print("%s left the chatroom." %name)
            break


clients = {}
addresses = {}

ENCODING = "utf8"
HOST = ''
PORT = 53000
BUFSIZE = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

