import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit


def linear_fit(x, slope, intercept):
    return x * slope + intercept


def inverse_linear_fit(y, slope, intercept):
    return (y - intercept) / slope


x_cg_bar = []
d_elevator_d_cl = []
with open(os.getcwd() + "/neutral_point_data.txt", "r") as f:
    data = [list(map(float, line.strip().split())) for line in f.readlines()[1:]]
print(data)

for i in data:
    x_cg_bar.append(i[0])
    d_elevator_d_cl.append(i[1])

print(x_cg_bar)
print(d_elevator_d_cl)

(slope, intercept), _ = curve_fit(linear_fit, x_cg_bar, d_elevator_d_cl)
neu_pt = inverse_linear_fit(0, slope, intercept)
x = np.linspace(min(x_cg_bar), neu_pt + 0.1 * neu_pt)
y = [linear_fit(x0, slope, intercept) for x0 in x]
plt.plot(x_cg_bar, d_elevator_d_cl, "-o")
plt.plot(x, y, "r--")
plt.title("dDelta_dCl vs x_cg_bar", fontweight="bold")
plt.xlabel("x_cg_bar", fontweight="bold")
plt.ylabel("dDelta_dCl", fontweight="bold")
plt.scatter(neu_pt, 0, c="k")
plt.annotate(
    f"Neutral Point: ({neu_pt}, 0)",
    (neu_pt, 0),
    (neu_pt * 0.98, -1.5),
    arrowprops=dict(arrowstyle="->", color="k"),
)
plt.legend(["Original Data", "Linear Extrapolation", "Neutral Point Location"])
plt.grid(True)
plt.show()
