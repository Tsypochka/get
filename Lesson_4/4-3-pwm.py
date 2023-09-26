import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

try:
    perc = int(input("Type percent: "))
    port = GPIO.PWM(24, 1000)
    port.start(perc)
    input("Press any key to stop")
    port.stop()
finally:
    GPIO.output(24, 0)
    GPIO.cleanup()