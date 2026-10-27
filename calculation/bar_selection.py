# import math


# def calculate_bar_area(diameter):
#     """Area 1 batang tulangan, mm2."""
#     return math.pi * diameter**2 / 4


# def select_main_rebar(
#     as_required,
#     diameter,
#     max_bars,
# ):
#     """
#     Preliminary bar selection.

#     Returns:
#         quantity
#         diameter
#         as_provided
#     """

#     if as_required <= 0:
#         raise ValueError("As required harus lebih dari 0.")

#     if diameter <= 0:
#         raise ValueError("Diameter harus lebih dari 0.")

#     if max_bars < 1:
#         raise ValueError("max_bars minimal 1.")

#     area_per_bar = calculate_bar_area(diameter)

#     quantity = math.ceil(as_required / area_per_bar)

#     if quantity > max_bars:
#         raise ValueError(
#             f"Kebutuhan {quantity} batang D{diameter} " f"melebihi max_bars={max_bars}."
#         )

#     as_provided = quantity * area_per_bar

#     return {
#         "quantity": quantity,
#         "diameter": diameter,
#         "area_per_bar": area_per_bar,
#         "as_provided": as_provided,
#     }


# bar selection baru


import math


def calculate_bar_area(diameter):
    return math.pi * diameter**2 / 4


def calculate_available_width(
    beam_width,
    cover,
    stirrup_diameter,
):
    # Clear width inside stirrups
    return beam_width - 2 * (cover + stirrup_diameter)


def calculate_bar_spacing(
    beam_width,
    cover,
    stirrup_diameter,
    bar_diameter,
    quantity,
):
    """
    Check one horizontal layer of bars.
    """

    if quantity < 1:
        return None

    available_width = calculate_available_width(
        beam_width,
        cover,
        stirrup_diameter,
    )

    if available_width <= 0:
        return None

    total_bar_width = quantity * bar_diameter

    remaining_width = available_width - total_bar_width

    if remaining_width < 0:
        return None

    if quantity == 1:
        clear_spacing = None
    else:
        clear_spacing = remaining_width / (quantity - 1)

    return {
        "available_width": available_width,
        "clear_spacing": clear_spacing,
        "fits": True,
    }


def select_main_rebar(
    as_required,
    beam_width,
    cover,
    stirrup_diameter,
    min_clear_spacing=25,
    max_bars=8,
    diameters=None,
):
    if as_required <= 0:
        raise ValueError("As_required harus > 0.")

    if diameters is None:
        diameters = [13, 16, 19, 22, 25]

    candidates = []

    for diameter in diameters:
        area = calculate_bar_area(diameter)

        for quantity in range(1, max_bars + 1):
            as_provided = area * quantity

            if as_provided < as_required:
                continue

            spacing = calculate_bar_spacing(
                beam_width=beam_width,
                cover=cover,
                stirrup_diameter=stirrup_diameter,
                bar_diameter=diameter,
                quantity=quantity,
            )

            if spacing is None:
                continue

            clear_spacing = spacing["clear_spacing"]

            # One bar is allowed geometrically here,
            # but not necessarily structurally valid.
            if quantity > 1 and clear_spacing < max(min_clear_spacing, diameter):
                continue

            candidates.append(
                {
                    "diameter": diameter,
                    "quantity": quantity,
                    "as_provided": as_provided,
                    "area_excess": as_provided - as_required,
                    "clear_spacing": clear_spacing,
                }
            )

    if not candidates:
        raise ValueError(
            "Tidak ditemukan kandidat tulangan. "
            "Periksa dimensi, As_required, atau batas kandidat."
        )

    # Preliminary selection:
    # smallest excess area first.
    candidates.sort(
        key=lambda x: (
            x["area_excess"],
            x["quantity"],
            x["diameter"],
        )
    )

    return candidates[0]
