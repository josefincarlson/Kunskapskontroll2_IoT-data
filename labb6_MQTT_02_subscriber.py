# ---------- Subscriber ----------
# Connect to HiveMQ Cloud and subscribe to your topic
# Note that MQTT is a real-time publish/subscribe-protocol

import paho.mqtt.client as mqtt
import json
import csv
import os

# MQTT Broker
broker = "38f4eadad3aa452a936329b3077a06d8.s1.eu.hivemq.cloud"
port = 8883
username = "picow"
password = "12345Qwerty"
topic = "room1/environment"

# CSV-file
filename = "iot_data.csv"

if not os.path.exists(filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "device_id", "voltage","min_val", "max_val", "level", "voltage", "decibel", "status"])


# Write to CSV on message
def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    print("Received:", data)

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            data["timestamp"],
            data["device_id"],
            data["voltage"],
            data["min_val"],
            data["max_val"],
            data["level"],
            data["decibel"],
            data["status"]
        ])

# MQTT callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(topic)


# MQTT client
client = mqtt.Client()
client.username_pw_set(username, password)
client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)

print("Listening for data...")

client.loop_forever()