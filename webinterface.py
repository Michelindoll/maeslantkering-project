import tornado.web, tornado.ioloop, os, datetime, db
from auth import cookieSecret
from pytz import timezone

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

        dummyData = db.SelectSensorDataFromDB()
        waterstandlist = []
        string = ''
        for item in dummyData:
            waterstandlist.append(item['waterstand'])
        for item in waterstandlist:
            string += str(item) + ','
        waterstandstring = string.rstrip(',')
        labellist = []
        string = ''
        for item in dummyData:
            labellist.append(datetime.datetime.fromtimestamp(int(item['tijd'])).strftime('%H:%M %d-%m-%Y '))
        for item in labellist:
            string += '\''+str(item) + '\','
        labelstring = string.rstrip(',')
        self.render("web/fluid/index.html",waterstandstring = waterstandstring, labelstring = labelstring)

class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/docs", DocsHandler),
            (r"/waterstand", WaterstandHandler),

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
