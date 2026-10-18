
import math


def calculate_effective_depth(
    beam,
    bar_diameter,
    stirrup_diameter
):
    """
    Menghitung effective depth d dalam mm.
    Asumsi: tulangan tarik berada di sisi bawah balok.
    """

    return (
        beam.height
        - beam.cover
        - stirrup_diameter
        - bar_diameter / 2
    )


def calculate_required_rebar(
    Mu,
    beam,
    parameters,
    bar_diameter,
    stirrup_diameter=10,
    phi=0.90
):
    """
    Mu dalam kN.m.
    Dimensi dalam mm.
    fc dan fy dalam MPa.
    Hasil As dalam mm².

    Asumsi awal:
    - Balok persegi dengan tulangan tarik tunggal.
    - Penampang terkendali tarik.
    - Tidak memperhitungkan tulangan tekan.
    """

    b = beam.width
    d = calculate_effective_depth(
        beam,
        bar_diameter,
        stirrup_diameter
    )

    fc = parameters.concrete.fc
    fy = parameters.reinforcement.fy

    # Konversi momen kN.m menjadi N.mm
    Mu_Nmm = Mu * 1_000_000

    # Persamaan:
    # phi * As * fy * (d - a/2) = Mu
    # a = As * fy / (0.85 * fc * b)
    #
    # Disusun menjadi persamaan kuadrat:
    # A*As² - B*As + C = 0

    A = (
        phi * fy**2
        / (2 * 0.85 * fc * b)
    )

    B = phi * fy * d
    C = Mu_Nmm

    discriminant = B**2 - 4 * A * C    

    if discriminant < 0:
        raise ValueError(
            "Momen terlalu besar untuk model "
            "penampang ini. Periksa dimensi "
            "atau gunakan desain penampang yang sesuai."
        )

    As = (
        B - math.sqrt(discriminant)
    ) / (2 * A)

    return {
        "Mu_kNm": Mu,
        "b_mm": b,
        "d_mm": d,
        "fc_MPa": fc,
        "fy_MPa": fy,
        "As_required_mm2": As,
    }


import math


def calculate_effective_depth(beam, bar_diameter, stirrup_diameter):
    """
    Menghitung tinggi efektif balok (d).
    Semua dimensi menggunakan mm.
    """
    return (
        beam.height
        - beam.cover
        - stirrup_diameter
        - bar_diameter / 2
    )


def calculate_minimum_rebar(
    beam,
    parameters,
    bar_diameter,
    stirrup_diameter=10
):
    """
    Menghitung luas tulangan lentur minimum.
    Rumus pendekatan ACI/SNI untuk balok nonprategang.
    """

    b = beam.width
    d = calculate_effective_depth(
        beam, bar_diameter, stirrup_diameter
    )

    fc = parameters.concrete.fc
    fy = parameters.reinforcement.fy

    if fc <= 0 or fy <= 0 or b <= 0 or d <= 0:
        raise ValueError(
            "fc, fy, lebar balok, dan tinggi efektif harus positif."
        )

    # Asumsi fc dan fy dalam MPa, b dan d dalam mm
    As_min_1 = 0.25 * math.sqrt(fc) / fy * b * d
    As_min_2 = 1.4 / fy * b * d

    As_min = max(As_min_1, As_min_2)

    return {
        "effective_depth_mm": d,
        "As_min_1_mm2": As_min_1,
        "As_min_2_mm2": As_min_2,
        "As_min_mm2": As_min,
    }



import math


def select_main_rebar(
    As_design,
    diameters=(10, 13, 16, 19, 22, 25, 29, 32),
    min_bars=2,
    max_bars=8
):
    """
    Memilih diameter dan jumlah tulangan berdasarkan luas baja.
    Belum memeriksa jarak bersih, lebar balok, atau detailing.
    """

    if As_design <= 0:
        raise ValueError("As_design harus lebih besar dari 0.")

    candidates = []

    for diameter in diameters:
        area_per_bar = math.pi * diameter**2 / 4

        for number_of_bars in range(min_bars, max_bars + 1):
            As_provided = number_of_bars * area_per_bar

            if As_provided >= As_design:
                candidates.append({
                    "diameter_mm": diameter,
                    "number_of_bars": number_of_bars,
                    "As_provided_mm2": As_provided,
                    "excess_mm2": As_provided - As_design,
                })

    if not candidates:
        raise ValueError(
            "Tidak ditemukan kombinasi tulangan. "
            "Perbesar max_bars atau tambahkan pilihan diameter."
        )

    # Pilih luas berlebih paling kecil.
    # Jika sama, pilih jumlah batang lebih sedikit.
    candidates.sort(
        key=lambda item: (
            item["excess_mm2"],
            item["number_of_bars"]
        )
    )

    return candidates[0]



def check_main_rebar_fit(
    beam,
    number_of_bars,
    bar_diameter,
    stirrup_diameter=10,
    min_clear_spacing=25
):
    """
    Memeriksa apakah tulangan utama muat dalam satu lapis.
    Semua dimensi dalam mm.

    min_clear_spacing harus ditentukan sesuai SNI yang berlaku
    dan ukuran agregat maksimum yang digunakan.
    """

    b = beam.width
    cover = beam.cover

    if number_of_bars < 1:
        raise ValueError("Jumlah tulangan minimal 1 batang.")

    if min(
        b, cover, bar_diameter, stirrup_diameter,
        min_clear_spacing
    ) <= 0:
        raise ValueError("Semua dimensi harus positif.")

    # Lebar bersih di antara sisi dalam kedua sengkang
    available_width = b - 2 * (cover + stirrup_diameter)

    # Lebar yang dibutuhkan batang dan jarak bersih antarb batang
    required_width = (
        number_of_bars * bar_diameter
        + (number_of_bars - 1) * min_clear_spacing
    )

    fits = required_width <= available_width

    return {
        "available_width_mm": available_width,
        "required_width_mm": required_width,
        "min_clear_spacing_mm": min_clear_spacing,
        "fits_one_layer": fits,
        "remaining_width_mm": available_width - required_width,
    }
