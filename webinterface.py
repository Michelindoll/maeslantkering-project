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
        self.render("web/fluid/index.html")

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
