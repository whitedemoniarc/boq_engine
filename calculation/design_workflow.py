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


from calculation.flexural_design import calculate_required_rebar
from calculation.bar_selection import select_main_rebar
from calculation.flexural_check import check_flexural_capacity


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
    # 1. Calculate required reinforcement
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
    # selection = select_main_rebar(
    #     as_required=as_required,
    #     diameter=main_bar_diameter,
    #     max_bars=max_bars,
    # )
    
    
    selection = select_main_rebar(
    as_required=as_required,
    beam_width=design_case.beam.width,
    cover=design_case.beam.cover,
    stirrup_diameter=stirrup_diameter,
    min_clear_spacing=25,
    max_bars=8,
    diameters=[13, 16, 19, 22, 25],
)


    # 3. Check provided reinforcement capacity
    check = check_flexural_capacity(
        design_case=design_case,
        as_provided=selection["as_provided"],
        fc=fc,
        fy=fy,
        phi=phi,
        stirrup_diameter=stirrup_diameter,
        main_bar_diameter=main_bar_diameter,
    )

    # 4. Save results
    result.as_required = as_required

    result.set_main_rebar(
        diameter=selection["diameter"],
        quantity=selection["quantity"],
        as_provided=selection["as_provided"],
    )

    result.status = check["status"]

    result.notes.append("Preliminary flexural capacity check only.")

    return result, check
