
from dataclasses import dataclass
from math import pi
from typing import Optional


@dataclass
class RebarLayer:
    quantity: int
    diameter: float
    y_from_bottom: float

    @property
    def area(self):
        return self.quantity * pi * self.diameter**2 / 4


def max_bars_per_layer(
    beam,
    diameter,
    stirrup_diameter=10,
    min_clear_spacing=25,
):
    """
    Kapasitas jumlah batang satu layer.
    Dimensi dalam mm.
    """
    available = (
        beam.width
        - 2 * (beam.cover + stirrup_diameter)
    )

    if diameter <= 0 or min_clear_spacing < 0:
        raise ValueError("Diameter harus positif dan spacing tidak negatif.")

    pitch = diameter + min_clear_spacing

    if available < diameter:
        return 0

    return max(
        0,
        int((available + min_clear_spacing) // pitch)
    )


def arrange_layers(
    beam,
    total_bars,
    diameter,
    stirrup_diameter=10,
    min_clear_spacing=25,
    min_vertical_clear_spacing=25,
    max_layers=4,
):
    """
    Membagi batang ke layer dengan jumlah layer minimum.
    Layer pertama berada paling dekat sisi bawah balok.

    Mengembalikan daftar RebarLayer atau error jika tidak muat.
    """
    if total_bars <= 0:
        raise ValueError("total_bars harus positif.")

    max_per_layer = max_bars_per_layer(
        beam,
        diameter,
        stirrup_diameter,
        min_clear_spacing,
    )

    if max_per_layer == 0:
        raise ValueError("Satu batang pun tidak muat dalam lebar balok.")

    for layer_count in range(1, max_layers + 1):
        if total_bars > layer_count * max_per_layer:
            continue

        # Isi layer bawah terlebih dahulu.
        quantities = []
        remaining = total_bars

        for _ in range(layer_count):
            qty = min(max_per_layer, remaining)
            quantities.append(qty)
            remaining -= qty

        if remaining:
            continue

        layers = []
        y = (
            beam.cover
            + stirrup_diameter
            + diameter / 2
        )

        for index, qty in enumerate(quantities):
            if index > 0:
                y += diameter + min_vertical_clear_spacing

            layers.append(
                RebarLayer(
                    quantity=qty,
                    diameter=diameter,
                    y_from_bottom=y,
                )
            )

        # Pastikan lapisan teratas masih berada dalam balok.
        if layers[-1].y_from_bottom + diameter / 2 > beam.height - beam.cover:
            continue

        return layers

    raise ValueError(
        "Tulangan tidak muat dengan batas jumlah layer. "
        "Periksa dimensi balok, diameter, cover, dan spacing."
    )


def calculate_capacity(
    beam,
    layers,
    parameters,
    stirrup_diameter=10,
    Es=200000,
    eps_cu=0.003,
    phi_tension=0.90,
    phi_compression=0.65,
):
    """
    Analisis penampang beton bertulang menggunakan strain compatibility.

    Asumsi awal:
    - Balok persegi.
    - Tulangan tarik berada di bawah.
    - Regangan beton tekan maksimum = 0.003.
    - Beton tarik diabaikan.
    - Tulangan berperilaku elastis-plastis.
    - phi_tension dan phi_compression merupakan input sementara.
    """

    b = beam.width
    h = beam.height
    fc = parameters.concrete.fc
    fy = parameters.reinforcement.fy

    if min(b, h, fc, fy, Es) <= 0:
        raise ValueError("Dimensi dan properti material harus positif.")

    # Ubah posisi dari bawah menjadi koordinat dari atas.
    steel = []

    for layer in layers:
        y_top = h - layer.y_from_bottom
        area_per_bar = pi * layer.diameter**2 / 4

        steel.append({
            "area": layer.quantity * area_per_bar,
            "y": y_top,
            "diameter": layer.diameter,
            "quantity": layer.quantity,
        })

    # Faktor beta1 pendekatan ACI/SNI untuk beton normal.
    beta1 = max(
        0.65,
        min(0.85, 0.85 - 0.05 * max(fc - 28, 0) / 7)
    )

    def section_state(c):
        a = min(beta1 * c, h)
        concrete_force = 0.85 * fc * b * a

        # Resultan beton tekan positif.
        force_residual = concrete_force
        moment_nmm = concrete_force * a / 2

        eps_t = 0.0

        for bar in steel:
            strain = eps_cu * (bar["y"] - c) / c
            stress = max(-fy, min(fy, Es * strain))
            force = bar["area"] * stress

            # Keseimbangan: beton tekan - resultan gaya baja.
            force_residual -= force

            # Momen terhadap sisi tekan atas.
            moment_nmm -= force * bar["y"]

            if strain > eps_t:
                eps_t = strain

        return force_residual, abs(moment_nmm), eps_t, a

    # Cari neutral axis dengan bisection.
    lo = 1e-4
    hi = h * 10

    f_lo = section_state(lo)[0]
    f_hi = section_state(hi)[0]

    if f_lo * f_hi > 0:
        raise ValueError(
            "Keseimbangan gaya tidak ditemukan. "
            "Periksa konfigurasi dan parameter material."
        )

    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = section_state(mid)[0]

        if abs(f_mid) < 1e-5:
            break

        if f_lo * f_mid <= 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid

    c = (lo + hi) / 2
    _, Mn_nmm, eps_t, a = section_state(c)

    # Faktor phi sederhana untuk ilustrasi.
    eps_y = fy / Es

    if eps_t >= 0.005:
        phi = phi_tension
    elif eps_t <= eps_y:
        phi = phi_compression
    else:
        phi = (
            phi_compression
            + (phi_tension - phi_compression)
            * (eps_t - eps_y)
            / (0.005 - eps_y)
        )

    return {
        "neutral_axis_mm": c,
        "a_mm": a,
        "Mn_kNm": Mn_nmm / 1_000_000,
        "phi": phi,
        "phi_Mn_kNm": phi * Mn_nmm / 1_000_000,
        "tensile_strain": eps_t,
        "layers": [
            {
                "quantity": layer.quantity,
                "diameter_mm": layer.diameter,
                "y_from_bottom_mm": layer.y_from_bottom,
                "area_mm2": layer.area,
            }
            for layer in layers
        ],
    }
