from classes.aircraft import Aircraft
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.stats import multivariate_normal as mn


def linear_fit(x, slope, intercept):
    return x * slope + intercept


def main():
    # Define Aircraft
    piper = Aircraft(name="Piper Saratoga HP II (VT-ETL)")

    # Assign reaction arms
    piper.assign_reaction_arms(nose_arm=14.2, port_arm=109.7, starboard_arm=109.7)

    # Add wing sections sequentially
    piper.add_wing_section(
        root_chord_length=71.6, tip_chord_length=65.5, section_span=27
    )
    piper.add_wing_section(
        root_chord_length=65.5, tip_chord_length=65.5, section_span=56
    )
    piper.add_wing_section(
        root_chord_length=65.5, tip_chord_length=45.5, section_span=108.6
    )

    # Group B Data
    pax_list = [0, 1, 2, 3, 4, 5]
    portside_reaction_list = [421, 450, 486, 544, 592, 620]
    nose_reaction_list = [310, 332, 321, 276, 266, 245]
    starboard_reaction_list = [420, 469, 519, 596, 629, 661]
    cg_bar_list = []

    print(f"{piper.name.upper()}")
    print("\n********** CG DATA **********")
    for pax, port, nose, starboard in zip(
        pax_list, portside_reaction_list, nose_reaction_list, starboard_reaction_list
    ):
        piper.assign_reactions(pax, port, nose, starboard)
        piper.calc_CG()
        print(f"\nNumber of Passengers: {piper.pax}")
        print(f"CG (inches): {piper.cg}")
        print(f"CG_bar: {piper.cg_bar}")
        cg_bar_list.append(piper.cg_bar)

    piper.wing.info()
    print(f"Mean Aerodynamic Chord of the entire wing (inches): {piper.wing.mac}")

    # Cruise
    piper.assign_engine_initial_values(2700, 29.92, 288.15, 300)
    velocity_list = [103, 103, 102, 97, 105, 79]
    rpm_list = [2130, 2110, 2110, 2110, 2110, 2660]
    temp_list = [34, 34, 34, 34, 35, 34]
    manifold_pressure_list = [21.4, 17.4, 20.5, 19.8, 21.6, 20.1]
    altitude_list = [2140, 1620, 1520, 1520, 1380, 1120]
    bhp_v_list = []

    for vel, rpm, temp, manif, alt in zip(
        velocity_list, rpm_list, temp_list, manifold_pressure_list, altitude_list
    ):
        piper.assign_operational_conditions(vel, rpm, manif, temp, alt)
        bhp_v_list.append(piper.engine.brake_horsepower_W * 0.514447 * vel)
    velocity_4_list = [(0.514447 * velocity) ** 4 for velocity in velocity_list]

    points = [(float(v), float(b)) for b, v in zip(bhp_v_list, velocity_4_list)]
    point_distances = [float(np.linalg.norm(point)) for point in points]
    mean, std = np.mean(point_distances), np.std(point_distances)
    z_score = np.abs((point_distances - mean) / std)
    threshold = 1.5
    good = z_score < threshold
    acceptable_x = []
    acceptable_y = []
    for i, goodness in enumerate(good):
        if goodness:
            acceptable_x.append(points[i][0])
            acceptable_y.append(points[i][1])

    print(points)
    print(point_distances)
    print(good)

    # Linear fit data
    (slope, y_intercept), _ = curve_fit(linear_fit, acceptable_x, acceptable_y)
    x = np.linspace(min(velocity_4_list), max(velocity_4_list), 50)
    y = [linear_fit(ab, slope, y_intercept) for ab in x]

    # Climb
    h_1_list = [
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        1600,
        1700,
        1800,
        1900,
    ]
    h_2_list = [
        500,
        600,
        700,
        800,
        900,
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        1600,
        1700,
        1800,
        1900,
        2000,
    ]
    speed1_list = [77, 77, 75, 76, 77, 82, 85, 83, 81, 96, 98, 97, 103, 101, 97, 101]
    speed2_list = [77, 75, 76, 77, 82, 85, 83, 81, 96, 98, 97, 103, 101, 97, 101, 102]
    time_list = [7, 7, 7, 12, 10, 10, 11, 11, 11, 16, 19, 12, 20, 11, 11, 17, 17]
    speed_list = []
    dh_dt_list = []
    gamma_list = []
    for h_1, h_2, time, s1, s2 in zip(
        h_1_list, h_2_list, time_list, speed1_list, speed2_list
    ):
        dh_dt = (h_2 - h_1) * 0.3048 / time
        s = (s1 + s2) * 0.5 * 0.5144447
        speed_list.append(s)
        dh_dt_list.append(dh_dt)
        gamma = np.arcsin((dh_dt / s)) * (180 / np.pi)
        gamma_list.append(float(gamma))
    print("\n********** FLIGHT CLIMB DATA **********")
    print(f"\nRates of climb (meters per second): {dh_dt_list}")
    print(f"\nClimb angles (degrees): {gamma_list}")

    print("\n********** FLIGHT CRUISE DATA **********\n")
    rho_list = [1.1549, 1.1687, 1.1687, 1.1756, 1.1826]
    wing_area = 16.16
    span = 10.9728
    AR = (span**2) / wing_area
    weight = 1609.6
    e_list = []
    for rho in rho_list:
        e = (2 * weight**2) / (y_intercept * AR * np.pi * rho * wing_area)
        e_list.append(float(e * 200))
    print(f"Curve Slope: {slope}")
    print(f"Y Intercept: {y_intercept}")
    print(f"Cd_0 values: {2*slope/([rho*wing_area for rho in rho_list])}")
    print(f"Oswald Efficiency Values: {e_list}")

    # plotting
    plt.scatter(velocity_4_list, bhp_v_list, marker="*")
    plt.plot(x, y, "r--")
    plt.title("B.H.P. * V vs V^4", fontweight="bold")
    plt.xlabel("V ^ 4 (m^4/s^4)", fontweight="bold")
    plt.ylabel("B.H.P. * V (watt meter / s)", fontweight="bold")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
