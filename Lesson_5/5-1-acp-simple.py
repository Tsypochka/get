import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
MaxVoltage = 3.3
levels = 2 ** len(dac)

GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def adc():
    for value in range(256):
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.005)
        compVal = GPIO.input(comp)
        if compVal == 1:
            return value
            break
try:
    while True:
        value = adc()
        if type(value) == int:
            voltage = value / levels * MaxVoltage
            print("Didgital = ", value, "Voltage = ", voltage)
        else:
            print("Mistake")
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()