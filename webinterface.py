import tornado.web, tornado.ioloop, os, datetime, db, zmq, time
from auth import cookieSecret

def GetWaterstandString(data):
    waterstandlist = []
    string = ''
    for item in data:
        waterstandlist.append(item['waterstand'])
    for item in waterstandlist:
        string += str(item) + ','
    waterstandstring = string.rstrip(',')
    return waterstandstring

def GetLabelString(data):
    labellist = []
    string = ''
    for item in data:
        labellist.append(datetime.datetime.fromtimestamp(int(item['tijd'])).strftime('%H:%M %d-%m-%Y '))
    for item in labellist:
        string += '\'' + str(item) + '\','
    labelstring = string.rstrip(',')
    return labelstring

def GetGraphData(locatie):
    data = db.SelectSensorDataFromDB(locatie)
    waterstand = GetWaterstandString(data)
    labels = GetLabelString(data)
    return waterstand, labels

def DoorControl(Action):
    #Verstuurt de actie naar de sluis
    if Action == 1:
        message = b'1'
    elif Action == 0:
        message = b'0'
    context = zmq.Context()
    print("Verbinden met sluisaansturing...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    print("Verzenden van verzoek...")
    socket.send(message)
    time.sleep(1)
    message = socket.recv()
    print(message.decode("ascii"))

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("web/index.html", title="Dashboard Waterdeur")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("web/login.html", title="Login")

    def post(self):
        logindata = db.getLoginCredentails()
        username = logindata[0]
        password = logindata[1]
        if self.get_argument("name") == username and self.get_argument("password") == password:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            pass

class DocsHandler(BaseHandler):
    def get(self):
        self.render("web/docs/index.html")

class WaterstandHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        maeslant = GetGraphData('Maeslantkering zeezijde N')
        rotterdam = GetGraphData('Rotterdam')
        dordrecht = GetGraphData('Dordrecht')
        self.render("web/fluid/index.html",WStringKering = maeslant[0], LString = maeslant[1], WStringRot = rotterdam[0], WStringDor = dordrecht[0],)

class ActionHandler(tornado.web.RequestHandler):
    def get(self):
        print("Noodsluiting")
        DoorControl(1)
        self.render("web/fluid/action.html")

class ActionHandler2(tornado.web.RequestHandler):
    def get(self):
        print("Noodsluiting")
        DoorControl(0)
        self.render("web/fluid/action.html")

class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/docs", DocsHandler),
            (r"/waterstand", WaterstandHandler),
            (r"/action-url", ActionHandler),
            (r"/action2-url", ActionHandler2)
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), ""),
            "cookie_secret": cookieSecret,
            "login_url": "/login",
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
