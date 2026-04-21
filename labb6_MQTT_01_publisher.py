# ---------- Publisher 2 ----------
# Read IoT-data and publish to broker/HiveMQ
# MicroPython

import network
import time
import math
from umqtt.simple import MQTTClient
from machine import ADC, Pin

# ---------------------------
# Device settings
# ---------------------------
device_id = "pico_1"

# WiFi
ssid = "Mindpark Guest" 
password = "SipAndSurf!"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print("Connected to WiFi")


# MQTT
broker = "38f4eadad3aa452a936329b3077a06d8.s1.eu.hivemq.cloud"
server_hostname = "38f4eadad3aa452a936329b3077a06d8.s1.eu.hivemq.cloud"
port = 8883
username = "picow"
password = "12345Qwerty"
topic = "room1/environment"

def connectMQTT():
    client = MQTTClient(client_id=b"pico_1",
         server=broker,
         port=port,
         user=username,
         password=password,
         keepalive=7200,
         ssl=True,
         ssl_params={'server_hostname': server_hostname})
    client.connect()
    return client

client = connectMQTT()
print("Connected to HiveMQ")


# ---------------------------
# Sensor - microphone on GP26
# ---------------------------
adc = ADC(Pin(26))

# Skicka data
def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("Publish done")
    
    
# ---------------------------
# Functions
# ---------------------------
def read_sound_level(samples=100, delay_ms=1):
    min_val = 65535
    max_val = 0

    for _ in range(samples):
        value = adc.read_u16()

        if value < min_val:
            min_val = value

        if value > max_val:
            max_val = value

        time.sleep_ms(delay_ms)

    level = max_val - min_val
    return min_val, max_val, level


def level_to_voltage(level, maxval=65535, v_ref=3.3):
    return (level / maxval) * v_ref


def level_to_decibel(level, maxval=65535, v_ref=3.3):
    """
    Relativt dB-värde baserat på signalnivå.
    Detta är inte riktiga dB i rummet.
    """
    voltage = level_to_voltage(level, maxval, v_ref)

    if voltage > 0:
        decibel = 20 * math.log10(voltage / v_ref)
    else:
        decibel = float("-inf")

    return decibel


def get_noise_label(level):
    if level <= 120:
        return "OK"
    elif level <= 400:
        return "VARNING"
    else:
        return "KRITISK"


def get_timestamp():
    """
    Enkel timestamp från Pico i sekunder sedan start.
    """
    return time.time()


def publish(topic, message):
    client.publish(topic, message)
    print("Published:", message)

# ---------------------------
# Main loop
# ---------------------------
while True:
    timestamp = get_timestamp()
    min_val, max_val, level = read_sound_level()
    voltage = level_to_voltage(level)
    decibel = level_to_decibel(level)
    label = get_noise_label(level)

    payload = '{{"timestamp": {}, "device_id": "{}", "voltage": {:.4f}, "min_val": {}, "max_val": {}, "level": {}, "decibel": {:.2f}, "status": "{}"}}'.format(
        timestamp,
        device_id,
        voltage,
        min_val,
        max_val,
        level,
        decibel,
        label
    )

    print(
        "timestamp:", timestamp,
        "device_id:", device_id,
        "min_val:", min_val,
        "max_val:", max_val,
        "level:", level,
        "voltage:", round(voltage, 4),
        "decibel:", round(decibel, 2),
        "status:", label
    )

    publish(topic, payload)
    time.sleep(2)