import machine
import time

adc = machine.ADC(machine.Pin(26))

def read_sound_level(samples=100, delay_ms=1):
    min_val = 65535
    max_val = 0

    for _ in range(samples):
        v = adc.read_u16()
        if v < min_val:
            min_val = v
        if v > max_val:
            max_val = v
        time.sleep_ms(delay_ms)

    level = max_val - min_val
    return min_val, max_val, level

while True:
    min_val, max_val, level = read_sound_level()
    print("Min:", min_val, "Max:", max_val, "Level:", level)
    time.sleep(0.5)