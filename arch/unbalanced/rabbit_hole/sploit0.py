import requests
import ipaddress

ip = "172.16.0.0/12"
url = "http://unbalanced.htb:3128/http://"


for t in ipaddress.IPv4Network(ip):
    temp = url + str(t)
    r = requests.post(temp)
    print(temp)
    if (r.status_code != 400):
        print('FOUND')
        print(temp)
        break


