import numpy as np
import matplotlib.pyplot as plt
with open('settings.txt', 'r') as set:
    settings = [float(i) for i in set.read().split("\n")]
data = np.loadtxt("data.txt", dtype=int)

data = data * settings[1] #acp data to volts
x = np.arange(1, len(data) + 1, 1, dtype=int)
x = x / settings[0] #number to seconds

fig, ax = plt.subplots(figsize=(16, 10), dpi=400)

ax.set_xlabel('Time, s')
ax.set_ylabel('Voltage, V')
plt.xlim(0, max(x) + 1)
plt.ylim(0, 2.8)
plt.title('Capacitor Charging and Discharging in RC circuit')

ax.plot(x, data, label='V(t)')
ax.scatter(x[1::3], data[1::3])
plt.legend()

plt.minorticks_on() #turn on minorsticks 

plt.grid(which='major')
plt.grid(which='minor', linestyle=':')
#add Charging/Discharging time
plt.text(6, 1, 'Charging time = 8.55 c')
plt.text(6, 0.9, 'Discharging time = 5.95 c')

fig.savefig("data_grafic.png")
plt.show()