import time
import zmq
import threading

a = 0

def connectionHandler():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        message = socket.recv()
        time.sleep(1)
        socket.send(b"rep")

def requestSender():
    global a
    context = zmq.Context()
    print("Zoeken naar ander meetstation...")
    socket = context.socket(zmq.REQ)
    socket.RCVTIMEO = 2000
    socket.connect("tcp://localhost:5555")
    socket.send(b"req")
    try:
        socket.recv()
        a = 1
    except:
        a = 2

threading.Thread(target=requestSender).start()

while a < 1:
    time.sleep(1)
if a == 1:
    print("Secundaire modus wordt gestart")
elif a == 2:
    print("Primaire modus wordt gestart")
    threading.Thread(target=connectionHandler()).start()
else:
    print("Het programma is niet goed gestart")
