from requests import put,get
import json

while True:
	state = raw_input("enter state you want off device")
	print "PUT"+put('http://localhost:5000/one',data={'id':"one" ,'state':state}).json()
