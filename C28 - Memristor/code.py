import numpy as np
import matplotlib.pyplot as plt

class BiolekMemristor:
    def __init__(self, Ron=100, Roff=16000, D=10e-9, uv=10e-14, x_init=0.1):
        self.Ron = Ron
        self.Roff = Roff
        self.D = D
        self.uv = uv
        self.x = x_init

    def window_function(self, x, I):
        if I > 0:
            return 1 - (x ** 2)
        else:
            return 1 - ((1 - x) ** 2)

    def update_state(self, V, dt):
        R = self.get_memristance()
        I = V / R
        dx = (self.uv * self.Ron * I / self.D**2) * self.window_function(self.x, I)
        self.x += dx * dt
        self.x = np.clip(self.x, 0, 1)

    def get_memristance(self):
        return self.Ron * self.x + self.Roff * (1 - self.x)

    def simulate(self, voltage_waveform, dt):
        current = []
        memristance = []
        time = []
        t = 0

        for V in voltage_waveform:
            R = self.get_memristance()
            I = V / R
            current.append(I)
            memristance.append(R)
            time.append(t)
            self.update_state(V, dt)
            t += dt

        return np.array(time), np.array(current), np.array(memristance), np.array(voltage_waveform)

# Simulation parameters
dt = 1e-5
t = np.arange(0, 0.1, dt)
v_in = 1.0 * np.sin(2 * np.pi * 50 * t)  # 50 Hz sinusoidal voltage

# Simulate memristor
memristor = BiolekMemristor()
time, current, memristance, voltage = memristor.simulate(v_in, dt)

# Plot I-V curve
plt.figure(figsize=(6, 6))
plt.plot(voltage, current, linewidth=1)
plt.title("Pinched Hysteresis Loop (I-V Curve)")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (A)")
plt.grid(True)
plt.tight_layout()
plt.show()
