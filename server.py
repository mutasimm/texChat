# SERVER

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


window = T.Tk()
window.title('TexChat:Server')
window.geometry('650x650')
window.resizable(False, False)

def ConnectionHandler(self):
    global Address
    global connectServer
    port1, port2 = Address.get().split()
    print(port1, port2)
    connectServer(int(port1), int(port2))

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

MsgView = T.Label(window, bg='grey')
MsgView.pack(fill='both')

MsgBox = T.Entry(window)
MsgBox.pack(fill=T.BOTH,side=T.BOTTOM)
MsgBox.bind('<Return>', SendHandler)


s = socket.socket()
t = socket.socket()
c1 = ''
c2 = ''
addr1 = ''
addr2 = ''

def receive():
    global c1
    global Updater
    while True:
        msg = c1.recv(1024).decode()
        Updater(msg)


def connectServer(port1, port2):
    global s
    global t
    global c1
    global c2
    global addr1
    global addr2
    global receive
    s.bind(('',port1))
    t.bind(('',port2))
    s.listen(100)
    t.listen(100)
    c1, addr1 = s.accept()
    print('server: 1st connection done')
    c2, addr2 = t.accept()
    print('server: 2nd connection done')
    threading.Thread(target=receive).start()


def Updater(msg):
    global MsgView
    global plt
    global processed_string
    msg = processed_string(msg)
    plt.clf()
    plt.axis('off')
    try:
        plt.text(0,1, msg,fontsize=12)
        plt.savefig('b.png', bbox_inches='tight')
    except:
        print('incorrect code...')
    image = ImageTk.PhotoImage(Image.open('b.png'))
    MsgView.configure(image=image, anchor=T.NW)
    MsgView.image = image


def send(msg):
    global c2
    c2.sendall(msg.encode())
    print('client: sent: ' + msg)


window.mainloop()
