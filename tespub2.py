import paho.mqtt.publish as publish
import json
import random
import time


def generate_emotion():
    emotions = ["normal", "hungry", "burping", "tired", "discomfort", "belly pain"]
    return random.choice(emotions)
'''
def create_data(id_alat, id_tambak):
    data = {
        "temp": random.randint(25, 33),
        "humd": str(random.randint(80, 100)),
        "emot": generate_emotion()
    }
    return json.dumps(data)
''' 

def data_to_send (id_alat, id_tambak):
    data = {
            "temp": avg_temperature,
            "humd": avg_humidity
            }
    return json.dumps(data)
                
def publish_data(data):
    publish.single('/raspi/incubator/final_project', data, qos=0,
                   hostname='broker.hivemq.com')
    print("Published data")

'''
def main():
    i = 9
    
        time.sleep(5)

if __name__ == "__main__":
    main()
'''

