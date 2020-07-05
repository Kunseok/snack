exec {memcache}<>/dev/tcp/localhost/11211
printf "stats items\nquit\n" >&${memcache}
cat <&${memcache} > myfile.txt
