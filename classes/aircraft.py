from classes.wing import WingSection, Wing
from classes.engine import Engine


class Aircraft:
    def __init__(
        self,
        name,
    ):
        self.name = name
        self.wing = Wing(WingSection(1, 1, 1))
        self.wing.wing_sections.clear()
        self.engine = Engine(-1, -1, -1, -1)  # Cessna 206H parameters
        self.cg = None
        self.cg_bar = None

    def assign_engine_initial_values(
        self,
        rated_rpm,
        rated_inlet_manifold_pressure_Hg,
        standard_air_temp_K,
        rated_horsepower_HP,
    ):
        self.engine = Engine(
            rated_rpm,
            rated_inlet_manifold_pressure_Hg,
            standard_air_temp_K,
            rated_horsepower_HP,
        )

    def assign_reaction_arms(self, nose_arm, port_arm, starboard_arm):
        self.nose_arm = nose_arm
        self.port_arm = port_arm
        self.starboard_arm = starboard_arm

    def assign_reactions(self, pax, port_reaction, nose_reaction, starboard_reaction):
        self.pax = pax
        self.nose_reaction = nose_reaction
        self.port_reaction = port_reaction
        self.starboard_reaction = starboard_reaction

    def assign_operational_conditions(
        self, velocity_kts, rpm, inlet_man_pr_Hg, air_temp_C, altitude_ft
    ):
        self.velocity_ms = velocity_kts * 0.5144
        self.altitude_m = altitude_ft * 0.304799
        self.engine.assign_operational_conditions(rpm, inlet_man_pr_Hg, air_temp_C)
        self.engine.calc_BHP()

    def calc_CG(self):
        self.cg = (
            self.port_arm * self.port_reaction
            + self.nose_arm * self.nose_reaction
            + self.starboard_arm * self.starboard_reaction
        ) / (self.port_reaction + self.nose_reaction + self.starboard_reaction)
        self.cg_bar = self.cg / self.wing.mac

    def add_wing_section(self, root_chord_length, tip_chord_length, section_span):
        self.wing.wing_sections.append(
            WingSection(root_chord_length, tip_chord_length, section_span)
        )
        self.wing = Wing(*self.wing.wing_sections)
