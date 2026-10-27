def check_flexural_capacity(
    design_case,
    as_provided,
    fc,
    fy,
    phi,
    stirrup_diameter,
    main_bar_diameter,
):
    beam = design_case.beam

    b = beam.width
    h = beam.height

    # Effective depth
    d = h - beam.cover - stirrup_diameter - main_bar_diameter / 2

    if b <= 0 or h <= 0 or d <= 0:
        raise ValueError("Dimensi balok tidak valid.")

    if fc <= 0 or fy <= 0 or phi <= 0:
        raise ValueError("Parameter material tidak valid.")

    if not 0 < phi <= 1:
        raise ValueError("phi harus > 0 dan <= 1.")

    if as_provided <= 0:
        raise ValueError("As_provided harus > 0.")

    # Compression block depth
    a = (as_provided * fy) / (0.85 * fc * b)

    # Nominal moment capacity
    Mn = as_provided * fy * (d - a / 2)

    # Design moment capacity
    phi_Mn = phi * Mn

    # Convert Nmm to kNm
    Mn_kNm = Mn / 1_000_000
    phi_Mn_kNm = phi_Mn / 1_000_000

    Mu_kNm = abs(design_case.mu)

    # Preliminary comparison only
    is_ok = phi_Mn_kNm >= Mu_kNm

    return {
        "a": a,
        "effective_depth": d,
        "Mn_kNm": Mn_kNm,
        "phi_Mn_kNm": phi_Mn_kNm,
        "Mu_kNm": Mu_kNm,
        "moment_margin_kNm": phi_Mn_kNm - Mu_kNm,
        "is_ok": is_ok,
        "status": ("PRELIMINARY_PASS" if is_ok else "PRELIMINARY_FAIL"),
    }
