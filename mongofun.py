import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

import json
import random
import string

class MongoFun:

    def __init__(self):
        """this function making connection to database"""

        try:
            self.conn = MongoClient('mongodb://localhost:27017/')
        except ConnectionFailure,e:
            sys.stderr.write("could not connect to MongoDb:%s"%e)
            sys.exit(1)
        self.db = self.conn['IOT']


    def FetchDbNames(self):
        """this function giving you all database name"""

        return self.conn.database_names()

    def SwitchDb(self,database):
        """this function is switching connection of database one-to other"""

        self.db=self.conn[database]
        print "you are currently on ",database
        return

    def GetCollection(self):
        """this database give you database collection names and that is really important"""
        return self.db.collection_names()

    def addUser(self,userData):
         self.db.users.insert(userData,safe=True)
         print "user is successfully inserted"
         return

    def addDevice(self,id,DeviceData):
        """function take 2 arguments email or id and DaviceData that genrated on main file
           ->first devices added to user.devices after,
           ->then create deivice database with deviceId
           ->assign fake data for to make collection
           ->in DeviceData there is two Field deviceid and devicekey"""

        self.db['users'].update({"_id":ObjectId(id)},{"$push":{"devices":DeviceData}})
        self.db.create_collection(DeviceData['deviceid'],size=1000000,max=100,capped=True)
        fakeData={"sensor":"temp","value":20}
        self.db[DeviceData['deviceid']].insert(fakeData,safe=True)
        return

    def verifyDevice(self,deviceid,devicekey):

        """function taking key and id as argument and if match than return true"""

        document=self.db['users'].find_one({"devices":{"$elemMatch":{"deviceid": deviceid,"devicekey":devicekey}}})

        if document:
            return 1
        else:
            return 0
        # for i in range(length):
        #     if document['devices'][i]['devicekey']==devicekey and document['devices'][i]['deviceid']==deviceid:
        #         return 1
        #     else:
        #         return 0

    def verifyUser(self,uname,pword):
        """ verify thae user with two parameter 1.username 2.password
        and if password is correct for username than return id if wrong retrun 0"""

        userinfo=self.db['users'].find_one({"email":uname})
        if userinfo is not None:
            document=userinfo
            if document['email']==uname and document['pass']==pword :
                print "document id",document['_id']
                return document['_id']
        else:
            return None




    def addDeviceStatus(self,device,status):
        """this function is add status to database when user submit data
           in websocket connection"""
        self.db[device].insert(status)
        return

    def getDeviceStatus(self,device,sensor):
        """get you a last status about the sensor"""

        status= self.db[device].find({"sensor":sensor}).limit(1).sort([["time",pymongo.DESCENDING]])
        for stat in status:
            del stat["_id"]
            return json.dumps(stat)
            break

    def randomGen(self,size,chars=string.ascii_uppercase+string.digits):
        """this function give randomize keys size that you passed to it"""

        return ''.join(random.choice(chars) for x in range(size))

    def listDevices(self,id):
        userinfo=self.db['users'].find_one({"_id":ObjectId(id)})
        if userinfo is not None:
            return userinfo['devices']




if __name__ == '__main__':
    """this is for testing function and all 'coz i hate unit testing """
    #test class __init__
    mongofun=MongoFun()

    #test FetchDbNames function
    print mongofun.FetchDbNames()

    #test GetCollection function
    print mongofun.GetCollection()

    #test add user in users database
    userData={ "name":"aniket patel",
              "email":"patelaniket165@gmail.com",
              "password":"!!@@##apAP90",
              "devices":[]
             }
    mongofun.addUser(userData)

    #test addDevice Function that add new device in users after genrating id and key
    #we genrate key here not programatically ,manuallly each key has 15 chars [alphanumeric]
    DeviceData={"deviceid":"1wWaItGHJ91EBngTHXet","devicekey":"aTijWhDFbcvDH146fdgr"}
    mongofun.addDevice("patelaniket165@gmail.com",DeviceData)

    #this test verify the verifyDevice function that need when before to connect database to collection of device
    # print mongofun.verifyDevice("aTijWhDFbcvDH146fdgr","1wWaItGHJ91EBngTHXet")

    #test of function addDeviceStatus
    statusdata={"sensor":"temp","value":20,"write":"device"}
    mongofun.addDeviceStatus("1wWaItGHJ91EBngTHXet",statusdata)
