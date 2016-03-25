import websocket
import thread
import time
import sys


def on_message(ws, message):
    print(message)
def on_error(ws, error):
    print(error)
def on_close(ws):
    print("connection closed")
def on_open(ws):
    def run(*args):
        for i in range(20):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            ws.send('{"method":"put","status":{"time":%d,"write" : "device","sensor" : "temp","value" : 20}}'%time.time())
            time.sleep(5)

        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    host = "ws://localhost:8888/ws?device=BCDMNQ15YUG5HG9O6OQG&key=SKALQ47QEFTA9A2"
    ws = websocket.WebSocketApp(host,on_message = on_message,on_error = on_error,on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()