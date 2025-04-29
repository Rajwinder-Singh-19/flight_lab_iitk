import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


class TrimElevator:
    def __init__(self, cg, cl_trim_list, delta_e_list):
        self.cg = cg
        self.cg_bar = self.cg / (1.49)
        self.cl_trim_list = cl_trim_list
        self.delta_e_list = delta_e_list
        assert len(cl_trim_list) == len(delta_e_list)
        (self.slope, _), _ = curve_fit(linear_fit, cl_trim_list, delta_e_list)


def linear_fit(x, slope, intercept):
    return slope * x + intercept


def inverse_linear_fit(y, slope, intercept):
    return (y - intercept) / slope


def main():
    #data_11 = TrimElevator(0.11, [0.3105, 0.3278, 0.3444], [2.9523, 2.667, -0.4953])
    data_11 = TrimElevator(0.11, [0.3105, 0.3278], [2.9523, 2.667])
    data_14 = TrimElevator(0.14, [0.4056, 0.4022, 0.4583], [1.7466, 1.8059, 1.1065])
    data_23 = TrimElevator(0.23, [0.3476, 0.3776, 0.3869], [3.1135, 2.696, 2.572])

    cg_bar_list = [data_11.cg_bar, data_14.cg_bar, data_23.cg_bar]
    slope_list = [data_11.slope, data_14.slope, data_23.slope]
    print([cg_bar for cg_bar in cg_bar_list])
    print([slope for slope in slope_list])

    (slope, intercept), _ = curve_fit(linear_fit, cg_bar_list, slope_list)

    #print(inverse_linear_fit(0, slope, intercept))

    (slope, intercept), _ = curve_fit(
        linear_fit, data_11.cl_trim_list, data_11.delta_e_list
    )
    x = np.linspace(min(data_11.cl_trim_list), max(data_11.cl_trim_list))
    y = linear_fit(x, slope, intercept)
    plt.scatter(data_11.cl_trim_list, data_11.delta_e_list, c="r")
    plt.plot(x, y, "r--")

    (slope, intercept), _ = curve_fit(
        linear_fit, data_14.cl_trim_list, data_14.delta_e_list
    )
    x = np.linspace(min(data_14.cl_trim_list), max(data_14.cl_trim_list))
    y = linear_fit(x, slope, intercept)
    plt.scatter(data_14.cl_trim_list, data_14.delta_e_list, c="b")
    plt.plot(x, y, "b--")

    (slope, intercept), _ = curve_fit(
        linear_fit, data_23.cl_trim_list, data_23.delta_e_list
    )
    x = np.linspace(min(data_23.cl_trim_list), max(data_23.cl_trim_list))
    y = linear_fit(x, slope, intercept)
    plt.scatter(data_23.cl_trim_list, data_23.delta_e_list, c="g")
    plt.plot(x, y, "g--")

    plt.title("Elevator deflection angle vs Cl trim", fontweight="bold")
    plt.xlabel("Cl trim", fontweight="bold")
    plt.ylabel("Elevator deflection angle (degrees)", fontweight="bold")
    plt.legend(
        [
            "Group ABC Data (CG - 11cm aft)",
            f"Group ABC Linear Fit - Slope: {data_11.slope}",
            "Provided Data (CG - 14cm aft)",
            f"Provided Linear Fit - Slope: {data_14.slope}",
            "Group DEF Data (CG - 23cm aft)",
            f"Group DEF Linear Fit - Slope: {data_23.slope}",
        ]
    )
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
