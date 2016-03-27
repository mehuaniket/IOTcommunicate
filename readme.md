###IOT COMMUNICATE
- following is structure of mongodb database that is very easy to understand 

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

- plus point of mongodb is we have not to stick with shema kinda thing.
- when user created account he trying to make new device server create them two key 
  - device unique id 
  - device auth key 

- that is used to make authenticated web socket connection
- following is url you have enter to connect our server make your device able to communcate over internet

```
                                   device-id              device-key
                                       ||                     ||

ws://localhost:8888/ws?device=MBIJ0R5BGXBDSYO0GIIE&key=SQC8JVFAL8NQRJS

```
- version 0.1 is ready we can say 
- example of client side version of python code is in iotdevice.py 
- user have make sign that update from device or client 
- that help server to make you notify about what changes need to be do on client side.
- server don't send data if data is write by server.
- you can user all sensor that have chunks of data or states use your programming skill to play with data and reflect on devices as you want 'coz we only f** iot information deliever' ;)