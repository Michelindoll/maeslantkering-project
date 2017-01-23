import time, zmq, threading

a = 0

def connectionHandler():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        message = socket.recv()
        time.sleep(0.1)
        socket.send(b"rep")

def requestSender():
    global a
    context = zmq.Context()
    print("Zoeken naar ander meetstation...")
    socket = context.socket(zmq.REQ)
    socket.RCVTIMEO = 1000
    socket.connect("tcp://localhost:5555")
    if a == 0 or a == 1:
        try:
            print(1)
            socket.send(b"req")
            #time.sleep(0.1)
            print(2)
            socket.recv()
            print(3)
            a = 1
        except:
            a = 2
            context.term()
        #else:
         #   context.term()

def DoorControl(Action):
    if Action == 1:
        message = b'1'
    elif Action == 0:
        message = b'0'
    context = zmq.Context()
    print("Kijk naar deur")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    print("Sending request …")
    socket.send(message)
    time.sleep(1)
    message = socket.recv()
    print(message.decode("ascii"))


threading.Thread(target=requestSender).start()

while a < 1:
    time.sleep(1)
if a == 1:
    print("Secundaire modus wordt gestart")
    while a == 1:
        threading.Thread(target=requestSender).start()
        print("Poll")
        time.sleep(1)
if a == 2:
    print("Primaire modus wordt gestart")
    threading.Thread(target=connectionHandler()).start()
else:
    print("Het programma is niet goed gestart")

print("idi nahui")

