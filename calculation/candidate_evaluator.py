from calculation.bar_selection import (
    calculate_bar_area,
    calculate_bar_spacing,
)
from calculation.flexural_check import (
    check_flexural_capacity,
)


def evaluate_main_rebar_candidates(
    design_case,
    as_required,
    fc,
    fy,
    phi,
    stirrup_diameter,
    min_clear_spacing=25,
    max_bars=8,
    diameters=None,
):
    beam = design_case.beam

    if diameters is None:
        diameters = [13, 16, 19, 22, 25]

    if as_required <= 0:
        raise ValueError("As_required harus > 0.")

    candidates = []
    rejected = []

    for diameter in diameters:
        if diameter <= 0:
            continue

        area = calculate_bar_area(diameter)

        for quantity in range(1, max_bars + 1):
            as_provided = area * quantity

            if as_provided < as_required:
                continue

            spacing = calculate_bar_spacing(
                beam_width=beam.width,
                cover=beam.cover,
                stirrup_diameter=stirrup_diameter,
                bar_diameter=diameter,
                quantity=quantity,
            )

            if spacing is None:
                continue

            clear_spacing = spacing["clear_spacing"]

            if quantity > 1 and clear_spacing < max(min_clear_spacing, diameter):
                continue

            # Capacity check
            check = check_flexural_capacity(
                design_case=design_case,
                as_provided=as_provided,
                fc=fc,
                fy=fy,
                phi=phi,
                stirrup_diameter=stirrup_diameter,
                main_bar_diameter=diameter,
            )

            candidate = {
                "diameter": diameter,
                "quantity": quantity,
                "as_provided": as_provided,
                "area_excess": as_provided - as_required,
                "clear_spacing": clear_spacing,
                "phi_Mn_kNm": check["phi_Mn_kNm"],
                "Mu_kNm": check["Mu_kNm"],
                "moment_margin_kNm": check["moment_margin_kNm"],
                "capacity_ok": check["is_ok"],
            }

            if check["is_ok"]:
                candidates.append(candidate)
            else:
                rejected.append(candidate)

    if not candidates:
        return {
            "selected": None,
            "candidates": [],
            "rejected": rejected,
            "status": "NO_CANDIDATE_PASSED",
        }

    # Preliminary ranking:
    # 1. Lowest excess steel area
    # 2. Fewer bars
    # 3. Smaller diameter
    candidates.sort(
        key=lambda x: (
            x["area_excess"],
            x["quantity"],
            x["diameter"],
        )
    )

    return {
        "selected": candidates[0],
        "candidates": candidates,
        "rejected": rejected,
        "status": "PRELIMINARY_PASS",
    }
