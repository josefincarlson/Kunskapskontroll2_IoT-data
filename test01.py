import machine
import time

#Set up the ADC pin for the microphone
adc = machine.ADC(machine.Pin(26))  # Replace with the correct pin

try:
    while True:
        # Read the ADC value
        adc_value = adc.read_u16()
        print(f"ADC Value: {adc_value}")  # Print the ADC value to the console
        time.sleep(0.5)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Stopping...")