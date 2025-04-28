class WingSection:
    def __init__(self, root, tip, span):
        self.root = root
        self.tip = tip
        self.ratio = self.tip / self.root
        self.span = span
        if self.root == self.tip:
            self.sec_type = "rectangular"
        elif self.root > self.tip:
            self.sec_type = "tapered"
        else:
            self.sec_type = "trapezoidal"
        self._assign_area()
        self._assign_mac()

    def _assign_area(self):
        self.area = 0.5 * (self.root + self.tip) * self.span

    def _assign_mac(self):
        self.mac = 2 / 3 * self.root
        t = self.ratio
        self.mac = self.mac * (1 + t + t**2)
        self.mac = self.mac / (1 + t)


class Wing:
    def __init__(self, *sections):
        self.wing_sections = []
        self.mac = 0.0
        for section in sections:
            self.wing_sections.append(section)
        self._assign_wing_mac()

    def _assign_wing_mac(self):
        sec_mac_list = []
        sec_area_list = []
        sec_span_list = []
        for section in self.wing_sections:
            sec_mac_list.append(section.mac)
            sec_area_list.append(section.area)
            sec_span_list.append(section.span)
        for mac, span in zip(
            sec_mac_list,
            sec_span_list,
        ):
            self.mac = self.mac + (mac**2) * (span)

        self.mac = self.mac / sum(sec_area_list)

    def info(self):
        sec_mac_list = []
        sec_area_list = []
        sec_span_list = []
        sec_type_list = []
        for section in self.wing_sections:
            sec_mac_list.append(section.mac)
            sec_area_list.append(section.area)
            sec_span_list.append(section.span)
            sec_type_list.append(section.sec_type)

        cumulative_span = 0
        span_sum = 0
        section_num = 0
        print("\n********** WING DATA **********\n")
        for mac, area, span, sec_type in zip(
            sec_mac_list, sec_area_list, sec_span_list, sec_type_list
        ):
            section_num = section_num + 1
            span_sum = span_sum + span
            print("Section", section_num)
            print("")
            print("section type:", sec_type)
            print("span (inches):", span)
            print("area (sq. inches):", area)
            print(f"mean aerodynamic chord of section {section_num} (inches):", mac)
            # print("integration lower limit (inches):", cumulative_span)
            # print("integration upper limit (inches):", span_sum)
            print("")
            cumulative_span = cumulative_span + span
