from requests import get

while True:
    print get('http://localhost:5000/one',data={'sensor':'temp'}).json()
