import math


def calculate_bar_area(diameter):
    """Area 1 batang tulangan, mm2."""
    return math.pi * diameter**2 / 4


def select_main_rebar(
    as_required,
    diameter,
    max_bars,
):
    """
    Preliminary bar selection.

    Returns:
        quantity
        diameter
        as_provided
    """

    if as_required <= 0:
        raise ValueError("As required harus lebih dari 0.")

    if diameter <= 0:
        raise ValueError("Diameter harus lebih dari 0.")

    if max_bars < 1:
        raise ValueError("max_bars minimal 1.")

    area_per_bar = calculate_bar_area(diameter)

    quantity = math.ceil(as_required / area_per_bar)

    if quantity > max_bars:
        raise ValueError(
            f"Kebutuhan {quantity} batang D{diameter} " f"melebihi max_bars={max_bars}."
        )

    as_provided = quantity * area_per_bar

    return {
        "quantity": quantity,
        "diameter": diameter,
        "area_per_bar": area_per_bar,
        "as_provided": as_provided,
    }
