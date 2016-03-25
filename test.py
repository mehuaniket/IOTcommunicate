from mongofun import MongoFun 
import pymongo
from pymongo import MongoClient
import time
import json
conn = MongoClient('mongodb://localhost:27017/')
db = conn['IOT']
coll=db['1wWaItGHJ91EBngTHXet']
deviceid= "1wWaItGHJ91EBngTHXet"
devicekey="asdfghjklasdkghjk"
# userinfo=db['users'].find({"devices":{"$elemMatch":{"deviceid" : "1wWaItGHJ91EBngTHXet"}}})
userinfo=db['users'].find({"devices":{"$elemMatch":{"deviceid": "1wWaItGHJ91EBngTHXet"}}})
for document in userinfo: 
    print document 
    length=len(document['devices'])
    for i in range(length):
        if document['devices'][i]['devicekey']==devicekey and document['devices'][i]['deviceid']==deviceid:
            print 1
        else:
            print 0
# cursor = coll.find({"time":{"$gt":time.time()}},await_data=True,tailable=True)     
# while cursor.alive:
#     try:
#         doc = cursor.next()
#         print doc
#     except StopIteration:
#         time.sleep(2)
# import time;

# while True:
#     print str(time.time())+"\n"
#     time.sleep(5)