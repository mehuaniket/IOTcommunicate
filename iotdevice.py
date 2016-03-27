import websocket
import thread
import time
import sys

info=False
query={}
def writebysign(write,sensor,value):
    global info
    global query
    info=True
    return ('{"method":"put","status":{"time":%d,"write":"%s","sensor" : "%s","value" : %d}}'%(time.time(),write,sensor,value))
def on_message(ws, message):
    print "[info]from message function:",message
def on_error(ws, error):
    print(error)
def on_close(ws):
    print "[notify] connection closed"
def on_open(ws):
    def run(*args):
        global query
        global info
        while True:
            if info is True:
                print "[info]ready query",query
                ws.send(query)
                info=False
            else:
                value=int(raw_input('enter value of temp=>'))
                sensor=raw_input('enter sensor id=>')
                write=raw_input('enter sign=>')
                query=str(writebysign(write,sensor,value))


            time.sleep(5)
        ws.close()
        print("[notify] Thread terminating")
    thread.start_new_thread(run, ())
if __name__ == "__main__":
    websocket.enableTrace(False)
    host = "ws://localhost:8888/ws?device=MBIJ0R5BGXBDSYO0GIIE&key=SQC8JVFAL8NQRJS"
    ws = websocket.WebSocketApp(host,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()