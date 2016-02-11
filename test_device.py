from requests import put,get
import json

while True:
	print "GET"+get('http://localhost:5000/one').json()
