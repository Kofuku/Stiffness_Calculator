from math import *
from collections import OrderedDict


class RCElement(object):

    shape = "rectangular"
    support = "simply supported"
    length = 0
    width = 0
    height = 0
    number_of_bars = 0
    diameter_of_bars = 0
    y_coordinate_of_bars = 0
    modulus_of_elasticity_concrete = 0
    modulus_of_elasticity_steel = 0
    load = 0
    force = {}
    bending_moment_additional = {}
    cracking_moment = 0

    number_of_forces = 0
    number_of_moments = 0

    support_reaction_a = 0
    support_reaction_b = 0

    steel_area = 0
    concrete_steel_ratio_coefficient = 0
    substitute_steel_area = 0
    compressive_height = 0

    moments_values = []

    def __init__(self, length, width, height, number_of_bars, diameter_of_bars, y_coordinate_of_bars,
                 modulus_of_elasticity_concrete, modulus_of_elasticity_steel, load, force, bending_moment_additional,
                 cracking_moment):
        self.length = length
        self.width = width
        self.height = height
        self.number_of_bars = number_of_bars
        self.diameter_of_bars = diameter_of_bars
        self.y_coordinate_of_bars = y_coordinate_of_bars
        self.modulus_of_elasticity_concrete = modulus_of_elasticity_concrete
        self.modulus_of_elasticity_steel = modulus_of_elasticity_steel
        self.load = load
        self.force = force
        self.bending_moment_additional = bending_moment_additional
        self.cracking_moment = cracking_moment
        self.geometric_additional()
        self.support_reaction_calculation()
        self.bending_moment_calculation()

    def geometric_additional(self):
        self.steel_area = (self.number_of_bars * ((pi * (self.diameter_of_bars / 2) ** 2)))
        self.concrete_steel_ratio_coefficient = (self.modulus_of_elasticity_steel / self.modulus_of_elasticity_concrete)
        self.substitute_steel_area = (self.concrete_steel_ratio_coefficient * self.steel_area)
        self.compressive_height = (self.height - self.y_coordinate_of_bars)

    def support_reaction_calculation(self):
        self.ordered_force = OrderedDict(sorted(self.force.items(), key=lambda x: x[0]))
        self.ordered_bending_moment_additional = OrderedDict(sorted(self.bending_moment_additional.items(),
                                                                    key=lambda x: x[0]))
        load_support_reaction = 0.5 * self.load * self.length
        self.number_of_forces = len(self.force)
        self.number_of_moments = len(self.bending_moment_additional)
        self.support_reaction_a = load_support_reaction
        self.support_reaction_b = load_support_reaction
        for force_distance in self.ordered_force:
            float_force_distance = float(force_distance)
            float_force_value = float(self.ordered_force[force_distance])
            self.support_reaction_a += (float_force_value -
                                            ((float_force_value * float_force_distance) / self.length))
            self.support_reaction_b += ((float_force_value * float_force_distance) / self.length)
        for bending_moment_distance in self.ordered_bending_moment_additional:
            float_bending_moment_add_value = float(self.ordered_bending_moment_additional[bending_moment_distance])
            self.support_reaction_a -= (float_bending_moment_add_value / self.length)
            self.support_reaction_b += (float_bending_moment_add_value / self.length)

    def bending_moment_calculation(self):
        self.moments_values = []
        for number_of_step in range(0, 101, 1):
            x_coordinate = ((self.length / 100) * number_of_step)
            step_moment_value = 0
            step_moment_value += ((self.support_reaction_a * x_coordinate) - (0.5 * (self.load * x_coordinate ** 2)))
            for force_step in self.ordered_force:
                float_force_step = float(force_step)
                float_force_value = float(self.ordered_force[force_step])
                if x_coordinate >= float_force_step:
                    step_moment_value -= (float_force_value * (x_coordinate - float_force_step))
            for moment_step in self.ordered_bending_moment_additional:
                float_moment_step = float(moment_step)
                float_moment_value = float(self.ordered_bending_moment_additional[moment_step])
                if x_coordinate >= float_moment_step:
                    step_moment_value += float_moment_value
            self.moments_values.append(step_moment_value)
