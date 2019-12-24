import paho.mqtt.client as paho
import time
from datetime import datetime
from elasticsearch import Elasticsearch
import json
from pprint import pprint
import pdb

es = Elasticsearch()

def send_to_es(msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    doc = {"topic" : msg.topic, "payload" : payload, "timestamp": datetime.utcnow()}
    res = es.index(index="zigbee2mqtt", doc_type='sensor', body=doc)
    print("----- send_to_es -----")
    pprint(res)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    print("----- on_message -----")
    pprint(msg.topic)
    payload = json.loads(msg.payload.decode('utf-8'))
    pprint(payload)
    send_to_es(msg)

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

client = paho.Client()
client.username_pw_set("zigbee2mqtt", "G7xZyM6g8H3Qeg3f")
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message
#client.connect("hassio.local", 1883, 60)
client.connect("192.168.16.152")
client.subscribe("zigbee2mqtt/#")
#client.subscribe("#")
client.loop_forever()
