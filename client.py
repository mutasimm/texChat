# client
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter as T
import socket
import threading

def processed_string(msg):
    n = len(msg)
    if n <= 60:
        return msg
    m = 0
    while m < n-1:
        msg = msg[:m]+'\n'+msg[m:]
        m += 60
    return msg
#print(processed_string('abdfasfasdfsdafsadfsdafsdafsafsadfsafsafdsdafsafsadfsadfsafsafdsafasdfasgsadgsdagsadfsafsadffsadgasdgsadgfsadgsdagsdagfsa'))

window = T.Tk()
window.title('TexChat:Client')
window.geometry('650x650')
#window.resizable(False, False)

def receive():
    global t
    global Updater
    while True:
        msg = t.recv(1024).decode()
        Updater(msg)

def ConnectionHandler(self):
    global Address
    global connectClient
    addr, port1, port2 = Address.get().split(' ')
    print(addr, port1, port2)
    connectClient(addr, int(port1), int(port2))

def SendHandler(self):
    global MsgBox
    global send
    msg = MsgBox.get()
    MsgBox.delete('0', T.END)
    send(msg)

Address = T.Entry(window)
Address.pack()
Address.bind('<Return>', ConnectionHandler)

Status = T.Label(window)
Status.pack()

#MsgView = T.Text(window)
MsgView = T.Label(window, bg='grey')
MsgView.pack(fill='both')


MsgBox = T.Entry(window)
MsgBox.pack(fill=T.BOTH, side=T.BOTTOM)
MsgBox.bind('<Return>', SendHandler)



s = socket.socket()
t = socket.socket()

def connectClient(addr, port1, port2):
    global s
    global t
    global receive
    s.connect((addr,port1))
    print('client: 1st connection done')
    t.connect((addr,port2))
    print('client: 2nd connection done')
    threading.Thread(target=receive).start()

def Updater(msg):
    global MsgView
    global plt
    global processed_string
    msg = processed_string(msg)
    plt.clf()
    plt.axis('off')
    #plt.figure(figsize=(.1,.1))
    try:
        plt.text(0,1, msg,fontsize=12)
        plt.savefig('a.png', bbox_inches='tight')
    except:
        print('Somethis went wrong...')
    MsgView.configure(image=image, anchor=T.NW)
    MsgView.image = image

def send(msg):
    global s
    s.sendall(msg.encode())
    print('client: sent: ' + msg)

window.mainloop()
