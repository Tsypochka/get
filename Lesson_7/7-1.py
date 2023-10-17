import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

troyka = 13
leds = [2, 3, 4, 17, 27, 22, 10, 9]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
MaxVoltage = 3.3
bites = len(dac)
levels = 2 ** bites
V_did = []
data_v = []
time_for_graf = []

GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

# функция - АЦП
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
    GPIO.output(leds, signal)
    return value_res

#функция, проверяющая зарядку/разрядку конденсатора, параллельно сохраняя значения напряжения и вывода АЦП
#limit - предел напряжения; direction = 1, значит ждём зарядки. direction = -1, значит ждём разрядки.
def charge_time(limit, direction):
    while True:
        value = adc()
        voltage = value / levels * MaxVoltage
        V_did.append(value)
        data_v.append(voltage)
        print("Voltage = ", voltage)
        time_for_graf.append(time.time() - start_time)
        if voltage >= limit and direction == 1:
            break
        if voltage < limit and direction == -1:
            break

try:
    start_time = time.time()
    GPIO.output(troyka, 1)
    charge_time(2.7, 1)
    GPIO.output(troyka, 0)
    charge_time(2.18, -1)
    finish_time = time.time()

    print("\n Time (с): ", finish_time - start_time)
    print("\n Частота дискретизации (Гц): ", len(V_did) / (finish_time - start_time))
    print("\n Шаг квантования АЦП (В): ", MaxVoltage / 256)
    
    V_str = [str(item) for item in V_did]
    with open("data.txt", "w") as f:
        f.write("\n".join(V_str))
    
    plt.plot(time_for_graf, data_v)
    plt.show()

    disc = str(len(V_did) / (finish_time - start_time))
    kvant = str(MaxVoltage / 256)
    with open("settings.txt", "w") as set:
        set.write("Частота дискретизации (Гц): " + disc)
        set.write("\n Шаг квантования АЦП (В): " + kvant)
finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()