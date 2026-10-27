from calculation.flexural_design import (
    calculate_required_rebar,
)

from calculation.bar_selection import (
    select_main_rebar,
)


def design_flexural_case(
    design_case,
    result,
    fc,
    fy,
    phi,
    stirrup_diameter,
    main_bar_diameter,
    max_bars=8,
):
    # 1. Calculate required As
    flexural = calculate_required_rebar(
        design_case=design_case,
        fc=fc,
        fy=fy,
        phi=phi,
        stirrup_diameter=stirrup_diameter,
        main_bar_diameter=main_bar_diameter,
    )

    as_required = flexural["as_required"]

    # 2. Select reinforcement
    selection = select_main_rebar(
        as_required=as_required,
        diameter=main_bar_diameter,
        max_bars=max_bars,
    )

    # 3. Store results
    result.as_required = as_required

    result.set_main_rebar(
        diameter=selection["diameter"],
        quantity=selection["quantity"],
        as_provided=selection["as_provided"],
    )

    result.status = "PRELIMINARY_ONLY"

    result.notes.append("Bar area selection only; full detailing checks pending.")

    return result
