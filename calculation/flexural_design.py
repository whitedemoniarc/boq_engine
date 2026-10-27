import math


def calculate_required_rebar(
    design_case,
    fc,
    fy,
    phi,
    stirrup_diameter,
    main_bar_diameter,
):
    """
    Preliminary flexural design.

    Units:
        fc, fy                 : MPa
        beam.width, height     : mm
        Mu                     : kNm
        diameters              : mm
        As                     : mm2

    Model:
        Rectangular section
        Singly reinforced
    """

    beam = design_case.beam

    b = beam.width
    h = beam.height

    # Determine tension face from design mark
    mark = design_case.mark.lower()

    if "atas" in mark:
        tension_face = "TOP"
    elif "bawah" in mark:
        tension_face = "BOTTOM"
    else:
        raise ValueError(f"Mark tidak dikenali: {design_case.mark}")

    # Effective depth
    # Assumes tension bars are in one layer
    d = h - beam.cover - stirrup_diameter - main_bar_diameter / 2

    if b <= 0 or h <= 0 or d <= 0:
        raise ValueError("Dimensi balok tidak valid.")

    if fc <= 0 or fy <= 0 or phi <= 0:
        raise ValueError("Parameter material/phi tidak valid.")

    if phi > 1:
        raise ValueError("phi harus lebih dari 0 dan <= 1.")

    # kNm to Nmm
    Mu = abs(design_case.mu) * 1_000_000

    if Mu == 0:
        return {
            "tension_face": tension_face,
            "effective_depth": d,
            "as_required": 0.0,
            "status": "PRELIMINARY_ONLY",
        }

    # phi * As * fy * (d - a/2) >= Mu
    #
    # a = As * fy / (0.85 * fc * b)
    #
    # Solve quadratic:
    # A*As^2 - B*As + Mu/phi = 0

    A = fy**2 / (2 * 0.85 * fc * b)
    B = fy * d

    discriminant = B**2 - 4 * A * (Mu / phi)

    if discriminant < 0:
        raise ValueError("Tidak ada solusi untuk model " "tulangan tarik tunggal ini.")

    As = (B - math.sqrt(discriminant)) / (2 * A)

    if As <= 0:
        raise ValueError("Hasil As tidak valid.")

    a = As * fy / (0.85 * fc * b)

    Mn = As * fy * (d - a / 2)

    return {
        "tension_face": tension_face,
        "effective_depth": d,
        "as_required": As,
        "a": a,
        "Mn_kNm": Mn / 1_000_000,
        "phi_Mn_kNm": phi * Mn / 1_000_000,
        "Mu_kNm": abs(design_case.mu),
        "status": "PRELIMINARY_ONLY",
    }
