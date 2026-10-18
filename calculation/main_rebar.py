from data.parameters import REBAR_UNIT_WEIGHT


class MainRebar:

    def __init__(
        self,
        mark,
        diameter,
        quantity,
        beam_length,
        # anchorage_left,
        # anchorage_right,
        # position
        anchorage_left=0,
        anchorage_right=0,
        position="BOTTOM",
    ):
        self.mark = mark
        self.diameter = diameter
        self.quantity = quantity
        self.beam_length = beam_length
        self.anchorage_left = anchorage_left
        self.anchorage_right = anchorage_right
        self.position = position

        

    @property
    def cutting_length(self):

        return (
            self.beam_length
            + self.anchorage_left
            + self.anchorage_right
        ) / 1000

    @property
    def total_length(self):

        return (
            self.quantity
            * self.cutting_length
        )

    @property
    def unit_weight(self):

        return REBAR_UNIT_WEIGHT[
            self.diameter
        ]

    @property
    def total_weight(self):

        return (
            self.total_length
            * self.unit_weight
        )
        
        
# Perhitungan berat besi utama (main rebar) menggunakan rumus:
# Berat Besi Utama (kg) = Panjang Total (m) x Berat Satuan (kg/m)

from data.parameters import REBAR_UNIT_WEIGHT


def calculate_main_rebar_weight(
    diameter,
    number_of_bars,
    cutting_length_mm
):
    """
    Menghitung panjang total dan berat tulangan utama.

    diameter        : diameter tulangan, misalnya 19 untuk D19
    number_of_bars  : jumlah batang
    cutting_length_mm : panjang potong per batang dalam mm
    """

    rebar_key = f"D{diameter}"

    if rebar_key not in REBAR_UNIT_WEIGHT:
        raise ValueError(
            f"Berat satuan {rebar_key} belum tersedia "
            "di data.parameters."
        )

    if number_of_bars <= 0 or cutting_length_mm <= 0:
        raise ValueError(
            "Jumlah batang dan panjang potong harus positif."
        )

    unit_weight = REBAR_UNIT_WEIGHT[rebar_key]

    cutting_length_m = cutting_length_mm / 1000
    total_length_m = number_of_bars * cutting_length_m
    total_weight_kg = total_length_m * unit_weight

    return {
        "diameter": rebar_key,
        "number_of_bars": number_of_bars,
        "cutting_length_per_bar_m": cutting_length_m,
        "total_length_m": total_length_m,
        "unit_weight_kg_per_m": unit_weight,
        "total_weight_kg": total_weight_kg,
    }
