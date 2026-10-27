from calculation.beam_design_result import BeamDesignResult


class BeamDesignEngine:
    def __init__(self, registry):
        self.registry = registry
        self.results = []

    def initialize_results(self):
        self.results = [
            BeamDesignResult(design_case=case)
            for case in self.registry.get_design_cases()
        ]

        return self.results
