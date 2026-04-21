import math

def adc_to_decibel(adc_value, maxval=65535, v0=3.3):
    # Beräkna den analoga spänningen
    voltage = (adc_value / maxval) * v0

#Beräkna dB
    if voltage > 0:  # För att undvika log(0), vilket är odefinierat
        decibel = 20 * math.log10(voltage / v0)
    else:
        decibel = float('-inf')  # Om spänningen är 0, sätt dB till minus oändlighet

    return decibel

#Exempelanvändning
adc_value = 2224  # Ange ditt ADC-värde här
decibel_value = adc_to_decibel(adc_value)

print(f"ADC-värde: {adc_value}, Decibel: {decibel_value:.2f} dB")