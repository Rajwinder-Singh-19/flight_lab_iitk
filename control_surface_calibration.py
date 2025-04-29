import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
import numpy as np

def linear_fit(x, slope, intercept):
    return x * slope + intercept


with open(os.getcwd() + "/pec_aileron.txt", "r") as f:
    data = [list(map(float, line.strip().split())) for line in f.readlines()[3:-2]]

angle_a = [i[0] for i in data]
voltage_a = [i[1] for i in data]

(slope, intercept), _ = curve_fit(linear_fit, angle_a, voltage_a)

x = np.linspace(min(angle_a), max(angle_a))
y = [linear_fit(x0, slope, intercept) for x0 in x]

plt.scatter(angle_a, voltage_a)
plt.plot(x, y, "--", color='red')
plt.title("PEC aileron calibration curve", fontweight="bold")
plt.xlabel("Deflection Angle (degrees)", fontweight="bold")
plt.ylabel("Voltage (Volts)", fontweight="bold")
plt.text(-4, 1, f"Slope: {slope: .4f}\nY Intercept: {intercept: .4f}", fontweight="bold")
plt.legend(["Observations", "Linear Curve Fit"])
plt.grid(True)
plt.show()
