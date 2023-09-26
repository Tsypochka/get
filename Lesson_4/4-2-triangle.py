import RPi.GPIO as GPIO
import time as t
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
try:
    period = int(input("Period = "))
    number = int(input("Number of periods = "))
    i = 0
    for j in range(number):
        while i < 255:
            GPIO.output(dac, decimal2binary(int(i)))
            print(3.3 / 256 * int(i))
            i = i + 1
            t.sleep(period / 512)
        while i > 0:
            GPIO.output(dac, decimal2binary(int(i)))
            print(3.3 / 256 * int(i))
            i = i - 1
            t.sleep(period / 512)
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()