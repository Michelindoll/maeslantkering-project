import time, zmq, threading, db, aes

mode = 0

#Functies:
def heartbeatHandler():
    #Reageert op de heartbeat's van het secundaire commandostation.
    #Als deze reactie niet ontvangen wordt wisselt het commandostation naar primaire modus.
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    while True:
        socket.recv()
        time.sleep(0.1)
        socket.send(b"reply")

def heartbeatSender():
    #Verstuurt een heartbeat naar het primaire commandostation.
    #Als de heartbeat niet beantwoord wordt schakeld het station om naar primaire modus.
    global mode
    context = zmq.Context()
    #print("Zoeken naar primair contolestation...")
    socket = context.socket(zmq.REQ)
    socket.RCVTIMEO = 1000
    socket.connect("tcp://localhost:5555")
    if mode == 0 or mode == 1:
        try:
            socket.send(b"req")
            socket.recv()
            mode = 1
        except:
            mode = 2
            context.term()

def DoorControl(Action):
    #Verstuurt de actie naar de sluis
    if Action == 1:
        message = aes.encryptData(b'1')
    elif Action == 0:
        message = aes.encryptData(b'0')
    context = zmq.Context()
    print("Verbinden met sluisaansturing...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    print("Verzenden van verzoek...")
    socket.send(message)
    time.sleep(1)
    message = socket.recv()
    print(message.decode("ascii"))

#Controleren of het primaire commandostation actief is.
#Als dit niet het het geval is zal deze instance als primary functioneren.
threading.Thread(target=heartbeatSender).start()

#Gun het programma een moment om te communiceren met het andere commandostation
print('Verbinding controleren...')
while mode < 1:
    time.sleep(1)

#Als het primaire commandostation actief wordt er naar secundaire modus geschakeld.
#In deze modus wordt elke seconde een heartbeat naar het primaire commandostation verstuurd.
#Wanneer hier geen reactie op komt schakeld het programma naar primaire modus.
if mode == 1:
    print("Secundaire modus wordt gestart")
    while mode == 1:
        threading.Thread(target=heartbeatSender).start()
        print("Heartbeat verzonden.")
        time.sleep(10)

#Start de primaire modus. Hier wordt de beslissing genomen om de kering te sluiten als er aan de criteria voldaan wordt.
#Tevens start de heartbeatHandler, die reacties geeft op de reacties van het secundaire controlestation
if mode == 2:
    print("Primaire modus wordt gestart")
    threading.Thread(target=heartbeatHandler).start()
    while True:
        while True:
            meting = db.SelectLastReadingFromDB("Dordrecht")
            meting2 = db.SelectLastReadingFromDB("Rotterdam")
            print("De huidige waterstand is %s cm onder of boven NAP in Dordrecht" % (meting[0]))
            print("De huidige waterstand is %s cm onder of boven NAP in Rotterdam" % (meting2[0]))
            if meting[0] > 300 and meting2[0] > 300:
                print('Waterstand overschreidt maximum, sluiting wordt in gang gezet.')
                threading.Thread(DoorControl(1)).start()
                break
            time.sleep(60)
        while True:
            meting = db.SelectLastReadingFromDB("Dordrecht")
            meting2 = db.SelectLastReadingFromDB("Rotterdam")
            print("De huidige waterstand is %s cm onder of boven NAP in Dordrecht" % (meting[0]))
            print("De huidige waterstand is %s cm onder of boven NAP in Rotterdam" % (meting2[0]))
            if meting[0] < 250 and meting2[0] < 250:
                print('Waterstand is gezakt tot een veilig punt, opening wordt in gang gezet.')
                threading.Thread(DoorControl(0)).start()
                break
            time.sleep(60)
print("End")


