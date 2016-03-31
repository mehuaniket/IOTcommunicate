import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

import socket
import time
import json
import os

import pymongo
from pymongo import MongoClient
from mongofun import MongoFun 
from bson.objectid import ObjectId

import thread

clients=[]
eventinject={}

'''
This is a file that handle is main in IOT communicate project 
'''
mongo=MongoFun()
class BaseHandler(tornado.web.RequestHandler):
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
    # mongo=MongoFun()
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        user=tornado.escape.xhtml_escape(self.current_user)
        self.render("newdevice.html")

    def post(self):
        global mongo
        self.id=self.current_user
        self.dname=self.get_argument('dname',True)
        self.did=mongo.randomGen(size=20)
        self.dkey=mongo.randomGen(size=15)
        DeviceData={"name":self.dname,"deviceid":self.did,"devicekey":self.dkey}
        mongo.addDevice(self.id,DeviceData)
        self.redirect("/mydevices")



class LogoutHandler(BaseHandler):
    '''for logout'''
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")      

class LoginHandler(BaseHandler):
    '''login handler'''
    # mongo=MongoFun()
    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render("login.html")

    def post(self):
        global mongo
        self.uname=self.get_argument('uname',True)
        self.pword=self.get_argument('pword',True)
        print "[notify]login from",self.uname
        id=str(mongo.verifyUser(self.uname,self.pword))
        print "[info]user loggedin",id
  
        if id is not "nid":
            self.set_secure_cookie("user",id)
            self.redirect("/")
        else:
            self.redirect("/login")

class MydeviceHandler(BaseHandler):
    '''my devices give list of devices that you created'''
    # mongo=MongoFun()
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.id=self.current_user
        devicelist=mongo.listDevices(self.id)
        self.render("home.html",mydevices=devicelist)

class DocsHandler(BaseHandler):
    '''provide docs to user'''
    # mongo=MongoFun()
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.id=self.current_user
        self.render("docs.html")


class  signUpHandler(tornado.web.RequestHandler):

    mongo=MongoFun()
    def get(self):
        self.render('signup.html')

    def post(self):
        global mongo
        self.name=self.get_argument('name',True)
        self.email=self.get_argument('email',True)
        self.pword=self.get_argument('pword',True)
        userData={"name":self.name,"email":self.email,"pass":self.pword,"devices":[]}
        mongo.addUser(userData)
        self.redirect("/login")



        
class WSHandler(tornado.websocket.WebSocketHandler):

    # mongo=MongoFun()
    def open(self):
        global mongo
        global clients
        global eventinject
        clients.append(self)
        self.device=self.get_argument('device',True)
        self.key=self.get_argument('key',True)
        self.side=self.get_argument('side',True)
        print "[notify]connection established",self.device
        print "[notify]from function in mongodbveriy",mongo.verifyDevice(self.device,self.key)
        if mongo.verifyDevice(self.device,self.key)==0:
            self.close()
        self.conn = MongoClient('mongodb://localhost:27017/')
        self.db = self.conn['IOT']
        self.coll = self.db[self.device]
        self.cursor = self.coll.find({"time":{"$gt":time.time()}},await_data=True,tailable=True)
        # self.write_message("conn opened") 
        def run(*args):
            while self.cursor.alive:
                try:
                    doc = self.cursor.next()
                    del doc["_id"]
                    if doc["write"]!=self.side:
                        self.write_message("\n==========from server========\n")
                        self.write_message(json.dumps(doc))
                except StopIteration:
                    time.sleep(2) 
        self.eventinject=thread.start_new_thread(run, ()) 
        # eventinject[self]=thread.start_new_thread(run, ()) 

        
    def on_message(self, message):
        #method put test query "{"method":"put","status":{"write" : "device","sensor" : "temp","value" : 20}}"
        opinfo=json.loads(message)
        print "[info]message received from",self.device
        if opinfo['method'] == "put":
            mongo.addDeviceStatus(self.device,opinfo["status"])
            self.write_message(u"from server added to database")
        elif opinfo['method']=="gets":
            self.write_message(mongo.getDeviceStatus(self.device,opinfo['sensor']))
        else:
            print "[fail]methods are not executed"
    def on_close(self):
        clients.remove(self)
        del eventinject[self]
        print("[notify]WebSocket closed")

settings = {
"template_path": os.path.join(os.path.dirname(__file__), "templates"),
"static_path":os.path.join(os.path.dirname(__file__), "static"),
"cookie_secret": "djbffdjgbkfdjsbgrkgkjtbrgbbfiurbt",
"xsrf_cookies": False,
"login_url": "/login",
"debug":True
}

application = tornado.web.Application(handlers=[
    (r'/docs',DocsHandler),
    (r'/',MainHandler),
    (r'/ws', WSHandler),
    (r'/login',LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/create', CreateHandler),
    (r'/mydevices', MydeviceHandler),
    (r'/signup', signUpHandler)
],**settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()
