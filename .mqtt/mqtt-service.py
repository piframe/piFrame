import paho.mqtt.client as paho
import time
from datetime import datetime
import json
from pprint import pprint
import pdb
import uuid
import subprocess


def send_to_es(msg):
    # topic = msg.topic
    # payload = msg.payload
    # payload = json.loads(msg.payload.decode('utf-8'))
    print("----- send_to_es -----")
    pprint(msg.topic)
    pprint(msg.payload)
    cmd = "vcgencmd display_power 1"
    if "on" in str(msg.payload):
        cmd = "vcgencmd display_power 1"
    if "off" in str(msg.payload):
        cmd = "vcgencmd display_power 0"
    res = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=True, universal_newlines=True, cwd='/tmp')

    pprint(res)


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_message(client, userdata, msg):
    print("----- on_message -----")
    pprint(msg.topic)
    # payload = json.loads(msg.payload.decode('utf-8'))
    # pprint(payload)
    send_to_es(msg)


# def on_publish(client, userdata, mid):
#    print("mid: "+str(mid))
print(hex(uuid.getnode()))

client = paho.Client()
client.username_pw_set("zigbee2mqtt", "G7xZyM6g8H3Qeg3f")
#client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.connect("hassio.local", 1883, 60)
client.connect("192.168.16.152")
client.subscribe("piframe/"+(hex(uuid.getnode()))+"/display_power")
#client.subscribe("#")
client.loop_forever()