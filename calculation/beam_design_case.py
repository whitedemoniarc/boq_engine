class BeamDesignCase:
    def __init__(
        self,
        beam,
        mark,
        mu,
        vu,
    ):
        self.beam = beam
        self.mark = mark
        self.mu = mu
        self.vu = vu

    @property
    def beam_type(self):
        return self.beam.name
