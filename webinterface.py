import tornado.web, tornado.ioloop, os
from auth import cookieSecret

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/index.html", title="Dashboard Waterdeur")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("web/login.html", title="Login")

    def post(self):
        logindata = ['Naam','Wachtwoord']
        username = logindata[0]
        password = logindata[1]
        if self.get_argument("name") == username and self.get_argument("password") == password:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            pass

class BeheerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("web/beheer.html")

class LightHandler(MainHandler):
    def get(self):
        self.render("web/light/index.html")

class IconnavHandler(MainHandler):
    def get(self):
        self.render("web/icon-nav/index.html")

class DocsHandler(MainHandler):
    def get(self):
        self.render("web/docs/index.html")

class FluidHandler(MainHandler):
    def get(self):

        dummyData = [{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50},{'waterstand':50}]
        var1 = dummyData[0]['waterstand']
        var2 = dummyData[1]['waterstand']
        var3 = dummyData[2]['waterstand']
        var4 = dummyData[3]['waterstand']
        var5 = dummyData[4]['waterstand']
        var6 = dummyData[5]['waterstand']
        var7 = dummyData[6]['waterstand']
        var8 = dummyData[7]['waterstand']
        var9 = dummyData[8]['waterstand']
        var10 = dummyData[9]['waterstand']
        var11 = dummyData[10]['waterstand']
        var12 = dummyData[11]['waterstand']
        self.render("web/fluid/index.html",var1 = var1, var2 = var2, var3 = var3, var4 = var4, var5 = var5, var6 = var6, var7 = var7, var8 = var8, var9 = var9, var10 = var10, var11 = var11, var12 = var12)

class OrderHistoryHandler(MainHandler):
    def get(self):
        self.render("web/order-history/index.html")

class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/beheer", BeheerHandler),
            (r"/light", LightHandler),
            (r"/iconnav", IconnavHandler),
            (r"/docs", DocsHandler),
            (r"/fluid", FluidHandler),
            (r"/orderhistory", OrderHistoryHandler),

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
