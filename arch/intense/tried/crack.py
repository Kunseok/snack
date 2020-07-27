# crack.py
import requests
from hashlib import sha256
from base64 import b64decode, b64encode
from random import randrange
import os

# generate data.digest
solution = "f1fc12010c094016def791e1435ddfdcaeccf8250e36630c0bc93285c2971105"
solution = solution.strip()

#target = "rockyou.txt"
target = "rockyou.txt"
f = open("/home/kali/wordlists/"+target, "r",errors="ignore")
for x in f:
    temp = x
    temp = temp.strip()
    test = sha256(temp.encode()).hexdigest()
    test = test.strip()
    print(test)
    if test == solution:
        print(temp)
        break

f.close()
