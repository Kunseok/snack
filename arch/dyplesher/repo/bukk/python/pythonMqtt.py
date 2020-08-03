import paho.mqtt.client as mqtt
import string
import sys

#out = client.publish('PLANET','radamar:mercury')
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("minecraft/#")

# the callback for when a publish message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_brake(client, userdata, msg):
    print("\nBRAKE", msg.topic+" "+str(msg.payload))

def on_place(client, userdata, msg):
    print("\nPLACE", msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.message_callback_add("minecraft/brake", on_brake)
    client.message_callback_add("minecraft/place", on_place)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    try:
        client.loop_forever()
    except keyboardinterrupt:
        sys.exit()
