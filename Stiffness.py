from RCElement import RCElement
from math import *


class Stiffness(object):

    rc_element = None
    uncracked_compressive_zone_height = 0
    cracked_compressive_zone_height = 0
    uncracked_moment_of_inertia = 0
    cracked_moment_of_inertia = 0

    def __init__(self, length, width, height, number_of_bars, diameter_of_bars, y_coordinate_of_bars,
                 modulus_of_elasticity_concrete, modulus_of_elasticity_steel, load, force, bending_moment_additional,
                 cracking_moment):
        self.rc_element = RCElement(length, width, height, number_of_bars, diameter_of_bars, y_coordinate_of_bars,
                 modulus_of_elasticity_concrete, modulus_of_elasticity_steel, load, force, bending_moment_additional,
                 cracking_moment)

    def effective_modulus_of_elasticity(self):
        pass

    def uncracked_compressive_zone_height_calculation(self):
        self.uncracked_compressive_zone_height = (((0.5 * self.rc_element.width * (self.rc_element.height ** 2)) +
                                        (self.rc_element.concrete_steel_ratio_coefficient * self.rc_element.steel_area *
                                         self.rc_element.compressive_height)) /
                                       ((self.rc_element.width * self.rc_element.height) +
                                    (self.rc_element.concrete_steel_ratio_coefficient * self.rc_element.steel_area)))

    def cracked_compressive_zone_height_calculation(self):
        self.cracked_compressive_zone_height = ((((-1) * self.rc_element.concrete_steel_ratio_coefficient *
                                                  self.rc_element.steel_area) +
                                        (sqrt(((self.rc_element.concrete_steel_ratio_coefficient ** 2) *
                                                    (self.rc_element.steel_area ** 2)) +
                                                   (2 * self.rc_element.concrete_steel_ratio_coefficient *
                                                    self.rc_element.steel_area * self.rc_element.width *
                                                (self.rc_element.height - self.rc_element.y_coordinate_of_bars))))) /
                                       (self.rc_element.width))

    def uncracked_moment_of_inertia_calculation(self):
        self.uncracked_moment_of_inertia = (((self.rc_element.width * (self.rc_element.height ** 3)) / 12) +
                                            (self.rc_element.width * self.rc_element.height *
                                             (((0.5 * self.rc_element.height) -
                                               self.uncracked_compressive_zone_height) ** 2) +
                                        (self.rc_element.concrete_steel_ratio_coefficient * self.rc_element.steel_area *
                                         (((self.rc_element.height - self.rc_element.y_coordinate_of_bars) -
                                           self.uncracked_compressive_zone_height) ** 2))))

    def cracked_moment_of_inertia_calculation(self):
        self.cracked_moment_of_inertia = (((self.rc_element.width * (self.cracked_compressive_zone_height ** 3)) / 3) +
                                 (self.rc_element.substitute_steel_area * (((self.rc_element.height -
                                                                             self.rc_element.y_coordinate_of_bars) -
                                                                        self.cracked_compressive_zone_height) ** 2)))

    stiffness_values = []

    def stiffness_calculation(self):
        self.stiffness_values = []
        for moment_value in self.rc_element.moments_values:
            if moment_value <= self.rc_element.cracking_moment:
                self.stiffness_values.append(self.rc_element.modulus_of_elasticity_concrete *
                                             self.uncracked_moment_of_inertia)
            else:
                self.stiffness_values.append((self.rc_element.modulus_of_elasticity_concrete *
                                              self.cracked_moment_of_inertia) /
                                             (1 - 0.5 * ((self.rc_element.cracking_moment /
                                                         moment_value) ** 2) *
                                             (1 - (self.cracked_moment_of_inertia / self.uncracked_moment_of_inertia))))
