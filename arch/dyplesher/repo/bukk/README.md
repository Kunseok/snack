# Minecraft IoT Server

1. Python
2. Mosquitto on [OSX](https://simplifiedthinking.co.uk/2015/10/03/install-mqtt-server/)
3. Scriptcraft with Craftbukkit

    +---------+    +---------------+   +-----------+    +----------------------------+
    | Python | => | mosquitto_pub |=> | mosquitto | => | scriptcraft => craftbukkit |
    +---------+    +---------------+   +-----------+    +----------------------------+
               ()                   (mqtt)          (mqtt)

## Running the Minecraft Server with support for MQTT

You can start the script `start.command` or run
```
java -Xmx1024M -classpath craftbukkit-1.8.jar:sc-mqtt.jar org.bukkit.craftbukkit.Main
```

## Python and MQTT

Make sure the mosquitto server is running then try the python script
```
python python/pythonMqtt.py
```
