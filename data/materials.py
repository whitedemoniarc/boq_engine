# class Concrete:
#     def __init__(self, name, fc, density=2400):
#         self.name = name
#         self.fc = fc
#         self.density = density


# class Reinforcement:
#     def __init__(self, name, fy, density=7850):
#         self.name = name
#         self.fy = fy
#         self.density = density

class Concrete:
    def __init__(
        self,
        name,
        fc,
        density=2400
    ):
        self.name = name
        self.fc = fc
        self.density = density


class Reinforcement:
    def __init__(
        self,
        name,
        fy,
        density=7850
    ):
        self.name = name
        self.fy = fy
        self.density = density
