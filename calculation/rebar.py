from data.parameters import REBAR_UNIT_WEIGHT


class Rebar:
    def __init__(self, mark, diameter, quantity, length, position):
        self.mark = mark
        self.diameter = diameter
        self.quantity = quantity
        self.length = length
        self.position = position

    @property
    def unit_weight(self):
        return REBAR_UNIT_WEIGHT[self.diameter]

    @property
    def total_length(self):
        return self.quantity * self.length

    @property
    def total_weight(self):
        return self.total_length * self.unit_weight
