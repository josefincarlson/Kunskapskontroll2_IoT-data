# ---------- Wifi ----------
# Connect your IoT-unit to wifi
# network-connection.py

import network
import time
ssid = "Mindpark Guest" 
password = "SipAndSurf!"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)