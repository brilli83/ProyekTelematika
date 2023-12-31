import paho.mqtt.client as mqtt
import base64
# import time
import pymongo
from datetime import datetime

#MQTT_SERVER = "192.168.150.202"
MQTT_SERVER = "broker.hivemq.com"
MQTT_PATH = "/raspi/incubator/final_project"
# MQTT_PATH2 = "/esp32camSensor"
# MQTT_PATH3 = "/pengeringMonitor"

# The callback for when the client receives a CONNACK response from the server.


# data
# id, temp. humd, emotion, time_stamp,


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH)
    # client.subscribe(MQTT_PATH3)

    # The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
    # more callbacks, etc
    # Create a file with write byte permission
    from datetime import datetime
    now = datetime.now()
    print(now)
    print(msg.payload)
    decoded_json = json.loads(msg.payload)

    temp = decoded_json["temp"]
    humd = decoded_json["humd"]
    emot = decoded_json["emot"]

    push_db(temp, humd, emot)
    # print(base64.b64decode(msg.payload))
    # f = open('2.jpg', "wb")
    # f.write(base64.b64decode(msg.payload))
    # print("Image Received")
    # f.close()


def push_db (temp, humd, emot):

    # Connect to MongoDB
    mongo_client = pymongo.MongoClient()

    # Get the database object
    db = mongo_client["my_database"]

    # Get the collection object
    collection = db["my_collection"]

    # Insert the data into the collection
    collection.insert_one({ "temp": temp, "humd": humd, "emot": emot, "date": Date() })

    # Close the MongoDB connection
    mongo_client.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
