from classes.aircraft import Aircraft
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np


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
    velocity_list = [114, 103, 78]
    rpm_list = [2120, 2110, 2140]
    temp_list = [34, 34, 34]
    manifold_pressure_list = [21.4, 19.9, 14.6]
    altitude_list = [2060, 1520, 1120]
    bhp_list = []

    for vel, rpm, temp, manif, alt in zip(
        velocity_list, rpm_list, temp_list, manifold_pressure_list, altitude_list
    ):
        piper.assign_operational_conditions(vel, rpm, manif, temp, alt)
        bhp_list.append(piper.engine.brake_horsepower_W)
    velocity_4_list = [velocity**4 for velocity in velocity_list]

    # Linear fit data
    (slope, y_intercept), _ = curve_fit(linear_fit, velocity_4_list, bhp_list)
    x = np.linspace(min(velocity_4_list), max(velocity_4_list), 50)
    y = [linear_fit(ab, slope, y_intercept) for ab in x]

    # Climb
    h_1_list = [1000, 1400, 1800]
    h_2_list = [1400, 1800, 2160]
    time_list = [50, 54, 61]
    dh_dt_list = []
    for h_1, h_2, time in zip(h_1_list, h_2_list, time_list):
        dh_dt = (h_2 - h_1) / time
        dh_dt_list.append(dh_dt)
    print("\n********** FLIGHT CLIMB DATA **********")
    print(f"\nRates of climb (feet per second): {dh_dt_list}")

    plt.plot(velocity_4_list, bhp_list, "--")
    plt.plot(x, y, color="r", marker=".")
    plt.scatter(velocity_4_list, bhp_list, marker="x")

    plt.title(
        "BHP * V vs V^4",
        fontweight="bold",
    )
    plt.legend(["Original", "Linear Fit"])
    plt.text(
        x=1.41e8,
        y=9.6e4,
        s=f"Slope: {slope: .4}\n\nY Intercept: {y_intercept: .4}",
        fontweight="bold",
    )
    plt.xlabel("V^4", fontweight="bold")
    plt.ylabel("BHP * V", fontweight="bold")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
