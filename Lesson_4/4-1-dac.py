import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
GPIO.setup(dac, GPIO.OUT)
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]
try:
    while True:
        a = input("Type numer from 0 to 255:")
        if a == "q":
            break
        if a.isdigit() is False:
            print("You've typed not a number or incorrect number")
        elif int(a) > 255:
            print("You've typed number bigger then 255")
        else:
            GPIO.output(dac, decimal2binary(int(a)))
            print(3.3 / 256 * int(a))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()