from requests import put,get
import json

while True:
    print get('http://localhost:5000/one',data={'sensor':'temp'}).json()
