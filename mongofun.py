import pymongo
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import json

class MongoFun:
   
    def __init__(self):
        """this function making connection to database"""
        try:
            self.conn = MongoClient('mongodb://localhost:27017/')
        except ConnectionFailure,e:
            sys.stderr.write("could not connect to MongoDb:%s"%e)
            sys.exit(1)   
        self.db = self.conn['IOT']
        assert self.db.connection == self.conn
    
    def FetchDbNames(self):
        """this function giving you all database name"""
        return self.conn.database_names()
    
    def SwitchDb(self,database):
        """this function is switching connection of database one-to other"""
        self.db=self.conn[database]
        print "you are currently on ",database

    def GetCollection(self):
        """this database give you database collection names and that is really important"""
        return self.db.collection_names()
     
    def addUser(self,userData):
        """this function is used when we have to insert new user"""
	self.db['users'].insert(userData,safe=True)
        print "user is successfully inserted"

    def addDevice(self,email,DeviceData):
        """function take 2 arguments email or id and DaviceData that genrated on main file
           ->first devices added to user.devices after,
           ->then create deivice database with deviceId
           ->assign fake data for to make collection
           ->in DeviceData there is two Field deviceid and devicekey"""
        self.db['users'].update({"email":email},{"$push":{"devices":DeviceData}})
        fakeData={"sensor":"temp","value":20}
        self.db[DeviceData['deviceid']].insert(fakeData,safe=True)     

    def verifyDevice(self,deviceid,devicekey):

        """function taking key and id as argument and if match than return true"""
        userinfo=self.db['users'].find({'devices.deviceid':deviceid})
        userinfo=json.loads(str(userinfo))
        print userinfo
        if userinfo['devices'][9].devicekey==devicekey:
            return 1
        else:
            return 0

    def addDeviceStatus(self,device,status):
        """this function is add status to database when user submit data in websocket connection"""
        self.db[device].insert(status,safe=True)  
        

    
if __name__ == '__main__':
    """this is for testing function and all 'coz i hate unit testing """
    #test class __init__
    mongofun=MongoFun()
    
    #test FetchDbNames function
    print mongofun.FetchDbNames()
    
    #test GetCollection function
    print mongofun.GetCollection()

    #test add user in users database
    userData={"email":"patelaniket165@gmail.com",
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
    
    
    
    
