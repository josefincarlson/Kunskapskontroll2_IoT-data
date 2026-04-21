# Blink with LED - "Hello world" for IoT
from machine import Pin
import time

led = Pin("LED", Pin.OUT)

while True:
    led.value(not led.value())
    TIME.SLEEP(0.5)