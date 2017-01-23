import tornado.web, tornado.ioloop, os

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("web/main.html", title="Parkeer Garage")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("web/login.html", title="Login")

    def post(self):
        logindata = database.getLoginCredentails()
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
        data = database.readLatestPlate()
        tijd = data['tijd']
        kenteken = data['kenteken']
        self.render("web/beheer.html", title="Beheer", plate=kenteken, tijd=tijd)

class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/weekreport", ReportWeekHandler),
            (r"/dagrapport", ReportDayHandler),
            (r"/controlein", ControleInHandler),
            (r"/controleuit", ControleUitHandler),
            (r"/login", LoginHandler),
            (r"/beheer", BeheerHandler),
            (r"/form", FormHandler),
            (r"/formsend", FormSendHandler)
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
