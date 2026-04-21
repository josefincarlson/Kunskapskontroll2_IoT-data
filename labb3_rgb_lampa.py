from machine import Pin, PWM
import time

red = PWM(Pin(2))
green = PWM(Pin(3))
blue = PWM(Pin(4))

for led in (red, green, blue):
    led.freq(1000)

def set_color(r, g, b):
    # 0–65535 i MicroPython PWM
    red.duty_u16(r)
    green.duty_u16(g)
    blue.duty_u16(b)

while True:
    set_color(65535, 0, 0)   # röd
    time.sleep(1)

    set_color(0, 65535, 0)   # grön
    time.sleep(1)

    set_color(0, 0, 65535)   # blå
    time.sleep(1)

    set_color(65535, 65535, 0)  # gul
    time.sleep(1)

    set_color(0, 0, 0)  # av
    time.sleep(1)