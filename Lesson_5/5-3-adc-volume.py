import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
MaxVoltage = 3.3
bites = len(dac)
levels = 2 ** bites

GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    value_res = 0
    temp_value = 0
    for i in range(bites):
        pow2 = 2 ** (bites - i - 1)
        temp_value = value_res + pow2
        signal = decimal2binary(temp_value)
        GPIO.output(dac, signal)
        time.sleep(0.005)
        compVal = GPIO.input(comp)
        if compVal == 0:
            value_res = value_res + pow2
    return value_res
try:
    while True:
        value = adc()
        voltage = value / levels * MaxVoltage
        print("Didgital = ", value, "Voltage = ", voltage)
        GPIO.output(leds, decimal2binary(value))
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()