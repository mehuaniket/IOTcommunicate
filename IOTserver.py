import socket
import time
import json
import os
import thread

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


import pymongo
from pymongo import MongoClient
from mongofun import MongoFun



clients = []
eventinject = {}

'''
This is a file that handle is main in IOT communicate project
'''
MONGO = MongoFun()


class BaseHandler(tornado.web.RequestHandler):
    """base handler no more use than fetch current user"""

    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    '''main handler check cookie if not valid than redirect to login'''

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.redirect('/mydevices')


class CreateHandler(BaseHandler):
    '''handler that create new devices with only by passing name in argument'''

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
       # user = tornado.escape.xhtml_escape(self.current_user)
        self.render("newdevice.html")

    def post(self):
        global MONGO
        self.id = self.current_user
        self.dname = self.get_argument('dname', True)
        self.did = MONGO.randomGen(size=20)
        self.dkey = MONGO.randomGen(size=15)
        DeviceData = {"name": self.dname,
                      "deviceid": self.did, "devicekey": self.dkey}
        MONGO.addDevice(self.id, DeviceData)
        self.redirect("/mydevices")


class LogoutHandler(BaseHandler):
    '''for logout'''

    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


class LoginHandler(BaseHandler):
    '''login handler'''

    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render("login.html")

    def post(self):
        global MONGO
        self.uname = self.get_argument('uname', True)
        self.pword = self.get_argument('pword', True)
        print "[notify]login from", self.uname
        id = MONGO.verifyUser(self.uname, self.pword)
        print "[info]user loggedin", str(id)

        if id is None:
            self.render("login.html")
        else:
            self.set_secure_cookie("user", str(id))
            self.redirect("/")


class MydeviceHandler(BaseHandler):
    '''my devices give list of devices that you created'''

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.id = tornado.escape.xhtml_escape(self.current_user)
        devicelist = MONGO.listDevices(self.id)
        self.render("home.html", mydevices=devicelist)


class DocsHandler(BaseHandler):
    '''provide docs to user'''

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.id = self.current_user
        self.render("docs.html")


class signUpHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('signup.html')

    def post(self):
        global MONGO
        self.name = self.get_argument('name', True)
        self.email = self.get_argument('email', True)
        self.pword = self.get_argument('pword', True)
        userdata = {"name": self.name, "email": self.email,
                    "pass": self.pword, "devices": []}
        MONGO.addUser(userdata)
        self.redirect("/login")


class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        global MONGO
        global clients

        clients.append(self)
        self.device = self.get_argument('device', True)
        self.key = self.get_argument('key', True)
        self.side = self.get_argument('side', True)
        print "[notify]connection established", self.device
        print "[notify]from function in mongodbveriy", MONGO.verifyDevice(self.device, self.key)
        if MONGO.verifyDevice(self.device, self.key) is 0:
            self.close()
        self.conn = MongoClient('mongodb://localhost:27017/')
        self.db = self.conn['IOT']
        self.coll = self.db[self.device]
        print "[notify]connection established"
        self.cursor = self.coll.find(
            {"time": {"$gt": time.time()}}, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)

        def run(*args):
            """it will run in background check for device update,if found then 
            sned it to respective device or client"""
            while self.cursor.alive:
                try:
                    doc = self.cursor.next()
                    del doc["_id"]
                    if doc["write"] != self.side:
                        self.write_message(json.dumps(doc))
                except StopIteration:
                    time.sleep(2)

        self.eventinject = thread.start_new_thread(run, ())

    def on_message(self, message):

        opinfo = json.loads(message)
        print "[info]message received from", self.device
        if opinfo['method'] == "put":
            opinfo["status"]["time"] = time.time()
            opinfo["status"]["write"] = self.side
            MONGO.addDeviceStatus(self.device, opinfo["status"])

        elif opinfo['method'] == "gets":

            self.write_message(MONGO.getDeviceStatus(
                self.device, opinfo['sensor']))

        else:

            print "[fail]methods are not executed"

    def on_close(self):

        clients.remove(self)
        print("[notify]WebSocket closed")


SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "djbffdjgbkfdjsbgrkgkjtbrgbbfiurbt",
    "xsrf_cookies": False,
    "login_url": "/login",
    "debug": True
}

application = tornado.web.Application(handlers=[
    (r'/docs', DocsHandler),
    (r'/', MainHandler),
    (r'/ws', WSHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/create', CreateHandler),
    (r'/mydevices', MydeviceHandler),
    (r'/signup', signUpHandler)
], **SETTINGS)

if __name__ == "__main__":
    Http_server = tornado.httpserver.HTTPServer(application)
    Http_server.listen(80)
    myip = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myip
    tornado.ioloop.IOLoop.instance().start()
