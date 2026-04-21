import machine
import time
import math

# Mikrofon på analog pin GP26
adc = machine.ADC(machine.Pin(26))

def read_sound_level(samples=100, delay_ms=1):
    """
    Läser mikrofonen flera gånger under en kort stund
    och räknar ut ljudnivån som skillnaden mellan
    högsta och lägsta uppmätta värde.
    """
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

def level_to_decibel(level, maxval=65535, v_ref=3.3):
    """
    Räknar om level-värdet till ett relativt dB-värde
    baserat på motsvarande spänning.

    Obs:
    Detta är inte en exakt ljudnivå i riktiga dB SPL,
    utan ett internt jämförelsevärde.
    """
    voltage = (level / maxval) * v_ref

    if voltage > 0:
        decibel = 20 * math.log10(voltage / v_ref)
    else:
        decibel = float("-inf")

    return decibel

def get_noise_label(level):
    """
    Klassificerar ljudnivån i tre nivåer
    baserat på tidigare testdata.
    """
    if level <= 120:
        return "OK"
    elif level <= 400:
        return "VARNING"
    else:
        return "KRITISK"

while True:
    min_val, max_val, level = read_sound_level()
    decibel = level_to_decibel(level)
    label = get_noise_label(level)

    print(
        "Min:", min_val,
        "Max:", max_val,
        "Level:", level,
        "dB:", round(decibel, 2),
        "Status:", label
    )

    time.sleep(0.5)