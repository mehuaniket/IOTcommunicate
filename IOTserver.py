from flask import Flask,request
from flask_restful import Resource,Api
import sqlite3
import json
import random
app = Flask(__name__)
api=Api(app)

app.debug=True

one={'id': "one",'state':"on"}
two={'id': "two",'state':"off"}
temp={}
@app.route('/')
def welocome():
    return '<center>welcome to IOT communicate!</center>'

class device(Resource):
    def get(self,device_id):
        # if request.form['sensor']=='temp':
        #     return json.dumps({"id":"one","state":random.randint(1,20)},sort_keys=True)
        # else:
        return json.dumps({"id":one['id'],"state":one['state']},sort_keys=True)

    def put(self,device_id):
        if request.method == 'PUT':
            one[device_id] = request.form['id']
            one['state'] = request.form['state']
            return "{\"id\":\""+one['id']+"\",\"state\":\""+one["state"]+"\"}"
            # return json.dumps({"id":one['id'],"state":one['state']},sort_keys=True)

api.add_resource(device,'/<string:device_id>')
if __name__ == '__main__':
    app.run(debug=True)
