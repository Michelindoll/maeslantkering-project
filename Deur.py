import zmq, time

def OpenDeur():
    #Doe Deur Openen
    return "Deur Openen"

def SluitDeur():
    #Do Deur Dicht
    return "Deur Sluiten"

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
while True:
    message = socket.recv()
    if message == 1:
        SluitDeur()
    elif message == 0:
        OpenDeur()
    time.sleep(1)
    socket.send(b"rep")
