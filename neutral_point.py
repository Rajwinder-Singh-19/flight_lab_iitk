import numpy as np
from scipy.optimize import curve_fit


class Graph_1_Data:
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
    data_11 = Graph_1_Data(0.11, [0.3105, 0.3278, 0.3444], [2.9523, 2.667, -0.4953])
    data_14 = Graph_1_Data(0.14, [0.4056, 0.4022, 0.4583], [1.7466, 1.8059, 1.1065])
    data_23 = Graph_1_Data(0.23, [0.3476, 0.346, 0.3869], [3.1135, 2.696, 2.572])

    cg_bar_list = [data_11.cg_bar, data_14.cg_bar, data_23.cg_bar]
    slope_list = [data_11.slope, data_14.slope, data_23.slope]

    (slope, intercept), _ = curve_fit(linear_fit, cg_bar_list, slope_list)

    print(inverse_linear_fit(0, slope, intercept))


if __name__ == "__main__":
    main()
