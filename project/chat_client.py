from queue import Full
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
import random
from tkinter import font


def receive_message():
    while True:
        try:
            # client waits for incoming messages on its socket
            msg = client_socket.recv(BUFSIZE).decode(ENCODING)
            # visualize all received messages on the screen
            # cursor must be at the end of the messages
            msg_list.insert(tkt.END,msg)
            # in case of error
        except OSError:
            break

def send_message(event=None):
    #events are managed by binders
    msg = my_msg.get()
    #free input
    my_msg.set("")
    #send message on socket
    client_socket.send(bytes(msg, ENCODING))
    if msg == "Q":
        client_socket.close()
        window.quit()

# utility used when the chat window is closed
def on_closing(event=None):
    my_msg.set("Q")
    send_message()

#-------GUI components---------

#window and frame
window = tkt.Tk()
window.title("Chatroom")

messages_frame = tkt.Frame(window)
messages_frame.pack()

#window background (random color given to each client)
color = random.randrange(0,2**24)
hexcolor = format(color, '06X')
window['bg'] = "#" + hexcolor

#scrollbar
scrollbar = tkt.Scrollbar(messages_frame)
scrollbar.pack(side=tkt.RIGHT,fill=tkt.Y)

#message list
msg_list = tkt.Listbox(messages_frame,height=20,width=80,yscrollcommand=scrollbar.set)
msg_list.config(font=font.Font(weight='bold'))
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH, )

#input field
my_msg = tkt.StringVar()
my_msg.set("...")

entry_field = tkt.Entry(window, width=40, font=('Arial',10), textvariable=my_msg)
entry_field.bind("<Return>", send_message)
entry_field.pack()

#send button
send_button = tkt.Button(window, text="Send",height=1,width=25,command=send_message)
send_button.pack(side=tkt.RIGHT, padx = 10, pady = 10)

#quit button and delete window protocol
quit_button = tkt.Button(window, text="Quit",height=1,width=25, command = on_closing)
quit_button.pack(side=tkt.LEFT, padx= 10, pady=10)
window.protocol("WM_DELETE_WINDOW", on_closing)

#-------Server Connection---------
HOST = input('Insert Host Server: ')
PORT = input('Insert Port Number of Host Server: ') 

if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZE = 1024
ENCODING = "utf8"
ADDR = (HOST,PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive_message)
receive_thread.start()
#activate chatroom GUI
tkt.mainloop()