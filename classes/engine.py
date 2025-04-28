class Engine:
    def __init__(
        self,
        rated_rpm,
        rated_inlet_manifold_pressure_Hg,
        standard_air_temp_K,
        rated_horsepower_HP,
    ):
        self.rated_rpm = rated_rpm
        self.rated_inlet_manifold_pressure_Pa = rated_inlet_manifold_pressure_Hg * 3386.38
        self.standard_air_temp_K = standard_air_temp_K
        self.rated_horsepower_W = rated_horsepower_HP * 745.6999

    def assign_operational_conditions(
        self, rpm, inlet_manifold_pressure_Hg, outside_air_temp_C
    ):
        self.rpm = rpm
        self.inlet_manifold_pressure_Pa = inlet_manifold_pressure_Hg * 3386.38
        self.outside_air_temp_K = outside_air_temp_C + 273.15

    def calc_BHP(self):
        self.brake_horsepower_W = (
            self.rpm
            * self.inlet_manifold_pressure_Pa
            * self.standard_air_temp_K
            * self.rated_horsepower_W
        )
        self.brake_horsepower_W = self.brake_horsepower_W / (
            self.rated_rpm
            * self.rated_inlet_manifold_pressure_Pa
            * self.outside_air_temp_K
        )
