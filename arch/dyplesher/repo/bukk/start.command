#!/bin/bash
#MY_PATH=$(dirname "$0") 
#TMP_DIR="tmp"

#cd "$MY_PATH"
#echo "$(pwd)"

#if [ -d "$TMP_DIR" ]; then
# echo "Reseting worlds"
# rm -vrf "world"
# cp -Rv "$TMP_DIR/world" .
#else
# echo "Backing up worlds"
# mkdir "$TMP_DIR"
# cp -Rv "world" "$TMP_DIR/"
#fi

java -Xmx1024M -classpath craftbukkit-1.8.jar:sc-mqtt.jar org.bukkit.craftbukkit.Main -o true 
#open -a Minecraft
#python python/mkmkServer.py
