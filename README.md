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
- Plus point of mongodb is we do not have to stick with shema thing.
  when user creats account,server provides new device key device id.
```
device unique id
device auth key
```
- That will use to make authenticated web socket connection.

- Following is url you have enter to connect server,this will make your device able to communicate over internet
 ```
                                   device-id              device-key
                                       ||                     ||

ws://localhost:8888/ws?device=MBIJ0R5BGXBDSYO0GIIE&key=SQC8JVFAL8NQRJS
```
## HOW to run Server

- TO run IOTCOMMUNICATE server file first you need to install pymongo,mongodb and other packages.

```bash
$ pip install pymongo
$ pip install tornado
```

```bash
pip install -r requirement.txt
```

- after this step you can directly run IOTserver.py by typing following command:
```bash
sudo python IOTserver.py
```
- After for test and understand the concept see documentation section in web, And don't forget make user table in mongodb with database name IOT, Otherwise it's gives you error because i did't use automatic creation of collection in project so you have to create this manually.
- To test client and device side you can run both file name iotdevice.py,iotclient.py after changing keys in URL!!
