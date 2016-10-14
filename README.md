# IOTcommunicate
middle communicator between your device to device(like arduino to mobile) by delivering chunks of information end to end!! 

following is structure of mongodb database that is very easy to understand
```
+---------+                +------------+
|device id|================|    temp    |->values
+---------+                +------------+
         ||                +------------+
         ||================|    led     |->values
         ||                +------------+
         ||================|other sensor|> 


+---------+               +-----------+
|  users  |===============|   email   |
+---------+               +-----------+
        ||                +-----------+
        ||================|   name    |
        ||                +-----------+
        ||                +-----------+  
        ||================|  password |
        ||                +-----------+
        ||                +-----------+
        ||================|  devices  |
                          +-----------+
```
plus point of mongodb is we have not to stick with shema kinda thing.
when user created account he trying to make new device server create them two key

device unique id
device auth key
that is used to make authenticated web socket connection

following is url you have enter to connect our server make your device able to communcate over internet
 ```
                                   device-id              device-key
                                       ||                     ||

ws://localhost:8888/ws?device=MBIJ0R5BGXBDSYO0GIIE&key=SQC8JVFAL8NQRJS
```
##HOW to run Server
- TO run IOTCOMMUNICATE server file first you need to install pymongo,mongodb and other package that you can see dependency by running file if i left sonthing here!!

```
pip install pymongo
```
- after this step you can directly run IOTserver.py by typing following command:
```
python IOTserver.py
```
- after for test and understand the concept see documentation section in web-interdace and don't forget make user table in mongodb database name IOT otherwise it's gives you error because i did't use automatic creation of collection in project so you have to create this manually.
- to test client and device side you can run both file name iotdevice.py,iotclient.py!!


version 0.1 is ready we can say
example of client side version of python code is in iotdevice.py
user have make sign that update is from device or client
that help server to make you notify about what changes need to be do on client side.
server don't send data if data is write by server.
you can user all sensor that have chunks of data or states use your programming skill to play with data and reflect on devices as you want 'coz we only f** iot information deliever' ;)
