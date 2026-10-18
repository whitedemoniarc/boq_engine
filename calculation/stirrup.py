import math
from data.parameters import (
    REBAR_UNIT_WEIGHT,
    STIRRUP_HOOK_135_EXTENSION  
) # Mengimpor kamus REBAR_UNIT_WEIGHT dan STIRRUP_HOOK_135_EXTENSION dari modul data.parameters, yang berisi berat per meter dan ekstensi kait untuk berbagai diameter besi stirrup


class Stirrup:  # Mendefinisikan kelas Stirrup, yang merepresentasikan besi stirrup dalam balok beton bertulang

    def __init__(              # Inisialisasi objek Stirrup dengan parameter yang diberikan
        self,                  # Merujuk pada instance dari kelas Stirrup yang sedang dibuat
        mark,                  # Kode tanda besi (misal: "ST1", "ST2")
        diameter,              # Diameter besi stirrup (misal: "D10", "D13", "D19")
        spacing,               # Jarak antar stirrup (mm)
        beam_width,            # Lebar balok (mm)
        beam_height,           # Tinggi balok (mm)
        beam_length,           # Panjang balok (mm)
        cover                  # Jarak pelindung besi (mm)
    ):
        self.mark = mark                # Kode tanda besi (misal: "ST1", "ST2")
        self.diameter = diameter        # Diameter besi stirrup (misal: "D10", "D13", "D19")
        self.diameter_mm = int(diameter.replace("D", "")) # Mengonversi diameter ke milimeter
        self.spacing = spacing          # Jarak antar stirrup (mm)

        self.beam_width = beam_width    # Lebar balok (mm)
        self.beam_height = beam_height  # Tinggi balok (mm)
        self.beam_length = beam_length  # Panjang balok (mm)

        self.cover = cover              # Jarak pelindung besi (mm)

    @property
    def quantity(self):
        return math.ceil(               # Menghitung jumlah stirrup yang dibutuhkan berdasarkan panjang balok dan jarak antar stirrup, kemudian membulatkan ke atas menggunakan fungsi math.ceil() untuk memastikan jumlah stirrup cukup
            self.beam_length / self.spacing 
        ) + 1

    @property
    def inner_width(self):
        return (
            self.beam_width
            - 2 * self.cover
            - self.diameter_mm
        )

    @property
    def inner_height(self):
        return (
            self.beam_height
            - 2 * self.cover
            - self.diameter_mm
        )

    @property
    def straight_length(self):

        return (
            2 * self.inner_width
            + 2 * self.inner_height
        )


    @property
    def hook_extension(self):

        return STIRRUP_HOOK_135_EXTENSION[
            self.diameter
        ]

    @property
    def cutting_length(self):

        return (
            self.straight_length
            + 2 * self.hook_extension
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





