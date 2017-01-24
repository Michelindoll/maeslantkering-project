import time, zmq
import nlalert

def SluitDeur():
    print("Deurtje Dicht")

def OpenDeur():
    print("Deurtje Open")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

while True:
    message = socket.recv()
    print("Received request: %s" % message)
    if message == b"1":
        SluitDeur()
        time.sleep(1)
        socket.send(b"Deur gaat sluiten")
        nlalert.sendAlert()
    elif message == b"0":
        OpenDeur()
        time.sleep(1)
        socket.send(b"Deur gaat open")
    else:
        pass


