import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import time
import json
from mongofun import MongoFun 

'''
This is a file that handle is main in IOT communicate project 
'''
mongo=MongoFun()
class WSHandler(tornado.websocket.WebSocketHandler):
    clients=[]
    global mongo
    def open(self):
        self.clients.append(self)
        self.device="1wWaItGHJ91EBngTHXet"
        print("WebSocket opened")
        
    def on_message(self, message):
        print "on message"
        opinfo=json.loads(message)
        print opinfo
        if opinfo['method'] == "put":
            print opinfo['status']
            mongo.addDeviceStatus(self.device,opinfo["status"])
            self.write_message(u"added to database")
        else:
            print "methods are not executed"
    def on_close(self):
        self.clients.remove(self)
        print("WebSocket closed")

application = tornado.web.Application([
    (r'/ws', WSHandler),
],debug=True)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()
