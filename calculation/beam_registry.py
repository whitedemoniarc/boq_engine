from calculation.beam import Beam
from calculation.beam_design_case import BeamDesignCase


class BeamRegistry:
    def __init__(self, beam_data, beam_design_data, parameters):
        self.beams = {}
        self.design_cases = []

        self._create_beams(beam_data, parameters)
        self._create_design_cases(beam_design_data)

    def _create_beams(self, beam_data, parameters):
        for beam_type, data in beam_data.items():
            self.beams[beam_type] = Beam(
                name=beam_type,
                width=data["width"],
                height=data["height"],
                length=data["length"],
                parameters=parameters,
            )

    def _create_design_cases(self, beam_design_data):
        for data in beam_design_data:
            beam_type = data["beam_type"]

            if beam_type not in self.beams:
                raise ValueError(
                    f"Tipe balok {beam_type} tidak ditemukan " "di BEAM_DATA."
                )

            case = BeamDesignCase(
                beam=self.beams[beam_type],
                mark=data["mark"],
                mu=data["mu"],
                vu=data["vu"],
            )

            self.design_cases.append(case)

    def get_beam(self, beam_type):
        return self.beams[beam_type]

    def get_design_cases(self, beam_type=None):
        if beam_type is None:
            return self.design_cases

        return [case for case in self.design_cases if case.beam_type == beam_type]
