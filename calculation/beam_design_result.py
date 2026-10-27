class BeamDesignResult:
    def __init__(
        self,
        design_case,
        as_required=None,
        as_provided=None,
        stirrup_required=None,
        status="NOT_DESIGNED",
        notes=None,
    ):
        self.design_case = design_case

        # Flexural design
        self.as_required = as_required
        self.as_provided = as_provided

        # Shear design
        self.stirrup_required = stirrup_required

        # Design status
        self.status = status
        self.notes = notes or []

    @property
    def beam(self):
        return self.design_case.beam

    @property
    def beam_type(self):
        return self.design_case.beam_type

    @property
    def mark(self):
        return self.design_case.mark

    @property
    def mu(self):
        return self.design_case.mu

    @property
    def vu(self):
        return self.design_case.vu
