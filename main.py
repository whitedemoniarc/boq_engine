# from calculation.beam import Beam


# beam = Beam(
#     name="B1",
#     width=400,
#     height=800,
#     length=6000,
#     cover=40
# )

# beam.add_main_rebar(
#     mark="B1-T",
#     diameter="D19",
#     quantity=4,
#     anchorage_left=400,
#     anchorage_right=400,
#     position="TOP"
# )


# beam.add_main_rebar(
#     mark="B1-B",
#     diameter="D19",
#     quantity=4,
#     anchorage_left=400,
#     anchorage_right=400,
#     position="BOTTOM"
# )

# beam.add_stirrup(
#     mark="B1-ST",
#     diameter="D10",
#     spacing=150
# )


# print()
# print("======================================")
# print("        BEAM REBAR SCHEDULE")
# print("======================================")

# for rebar in beam.main_rebars:

#     print(
#         f"{rebar.mark:<8}"
#         f"{rebar.position:<10}"
#         f"{rebar.diameter:<6}"
#         f"{rebar.quantity:>4} pcs   "
#         f"{rebar.cutting_length:.2f} m   "
#         f"{rebar.total_weight:.2f} kg"
#     )

# for stirrup in beam.stirrups:

#     print(
#         f"{stirrup.mark:<8}"
#         f"{'STIRRUP':<10}"
#         f"{stirrup.diameter:<6}"
#         f"{stirrup.quantity:>4} pcs   "
#         f"{stirrup.cutting_length:.2f} m   "
#         f"{stirrup.total_weight:.2f} kg"
#     )

#     print("--------------------------------------")
#     print(
#     f"TOTAL REBAR = "
#     f"{beam.total_rebar_weight:.2f} kg"
#     )
# # clear the console

#     print()
#     print(f"Mark             : {stirrup.mark}")
#     print(f"Diameter         : {stirrup.diameter_mm} mm")
#     print(f"Spacing          : {stirrup.spacing} mm")
#     print(f"Quantity         : {stirrup.quantity} pcs")

#     print()

import subprocess
import os

from data.materials import Concrete, Reinforcement
from data.design_parameters import DesignParameters


concrete = Concrete(name="K400", fc=40)

reinforcement = Reinforcement(name="BJTS 420", fy=420)

parameters = DesignParameters(
    concrete=concrete, reinforcement=reinforcement, beam_cover=40
)


from calculation.beam import Beam


beam = Beam(
    name="B1",
    width=400,
    height=800,
    length=6000,
    #cover=40
    parameters=parameters
)


beam.add_main_rebar(
    mark="B1-TA",
    diameter=19,
    quantity=4,
    anchorage_left=400,
    anchorage_right=400,
    position="TOP"
)


beam.add_main_rebar(
    mark="B1-TB",
    diameter=19,
    quantity=4,
    anchorage_left=400,
    anchorage_right=400,
    position="TOP"
)

beam.add_main_rebar(
    mark="B1-LA",
    # b_lebar_mm=beam.width,
    # h_tinggi_mm=beam.height,
    diameter=19,
    quantity=4,
    anchorage_left=400,
    anchorage_right=400,
    position="BOTTOM"
)

beam.add_main_rebar(
    mark="B1-LB",
    # b_lebar_mm=beam.width,
    # h_tinggi_mm=beam.height,
    diameter=19,
    quantity=4,
    anchorage_left=400,
    anchorage_right=400,
    position="BOTTOM"
)

beam.add_stirrup(
    mark="B1-ST",
    diameter="D10",
    spacing=150,
)

beam.add_stirrup(
    mark="B1-SL",
    diameter="D10",
    spacing=150
)

from data.materials import (
    Concrete,
    Reinforcement
)

from data.design_parameters import (
    DesignParameters
)


concrete = Concrete(
    name="K400",
    fc=40
)

reinforcement = Reinforcement(
    name="BJTS 420",
    fy=420
)

parameters = DesignParameters(
    concrete=concrete,
    reinforcement=reinforcement,
    beam_cover=40
)

print("CONCRETE")
print(
    f"{parameters.concrete.name}: "
    f"{parameters.concrete.fc} MPa"
)

print()

print("REINFORCEMENT")
print(
    f"{parameters.reinforcement.name}: "
    f"{parameters.reinforcement.fy} MPa"
)

# print(beam.cover)

print()

print(
    "BEAM COVER:",
    parameters.beam_cover,
    "mm"
)

print()
print("======================================")
print("        BEAM REBAR SCHEDULE")
print("======================================")

print(f"Beam       : {beam.name}")
print(f"Dimension  : " f"{beam.width} x {beam.height} mm")
print(f"Length     : {beam.length / 1000:.2f} m")
print(f"Cover      : {beam.cover} mm")

print()
print(
    f"{'MARK':<10}"
    f"{'POS':<10}"
    f"{'B (mm)':>10} "
    f"{'H (mm)':>10} "
    f"{'BAR':<8}"
    f"{'QTY':>8}"
    f"{'LENGTH':>12}"
    f"{'WEIGHT':>12}"
)

print("-" * 64)


for rebar in beam.main_rebars:

    print(
        f"{rebar.mark:<10}"
        f"{rebar.position:<10}"
        f"{rebar.beam.width:>10} "
        f"{rebar.beam.height:>10} "
        # f"{rebar.diameter:<6}"
        f"{'D' + str(rebar.diameter):<8}"
        f"{rebar.quantity:>5}  "
        f"{ 'pcs'  :>4}"
        f"{f'{rebar.cutting_length_m:.2f} m':>12}"
        f"{f'{rebar.total_weight:.2f} kg':>12}"  
        # f"{(f'{rebar.cutting_length_m:.2f} m')  :>12}"
        # f"{f'{rebar.total_weight:.2f} kg':>12}"
        # f"{rebar.total_weight:.2f} kg"
    )


for stirrup in beam.stirrups:

    print(
        f"{stirrup.mark:<10}"
        f"{'STIRRUP':<10}"
        f"{beam.width:>10} "
        f"{beam.height:>10} "
        f"{stirrup.diameter:<8}"
        f"{stirrup.quantity:>5}  "
        # f"{(str(stirrup.quantity) + ' pcs'):>8}"
        f"{ 'pcs'  :>4}" 
        # f"{stirrup.cutting_length:.2f} m   "
        # f"{stirrup.total_weight:.2f} kg"
        f"{(f'{stirrup.cutting_length:.2f} m'):>12}"
        f"{(f'{stirrup.total_weight:.2f} kg'):>12}"
    )


print("-" * 64)

print(
    f"TOTAL REBAR = "
    f"{beam.total_rebar_weight:.2f} kg"
)

print()
print("QUANTITY")
print("------------------------------------------")

print(
        f"Total Length     : "
        f"{stirrup.total_length:.2f} m"
    )

print(
        f"Unit Weight      : "
        f"{stirrup.unit_weight:.3f} kg/m"
    )

print(
        f"Total Weight     : "
        f"{stirrup.total_weight:.2f} kg"
    )

print()
print("GEOMETRY")
print("------------------------------------------")

print(
        f"Inner Width      : "
        f"{stirrup.inner_width:.0f} mm"
    )

print(
        f"Inner Height     : "
        f"{stirrup.inner_height:.0f} mm"
    )

print(
        f"Straight Length  : "
        f"{stirrup.straight_length:.0f} mm"
    )

print(
        f"Hook Extension   : "
        f"{stirrup.hook_extension:.0f} mm × 2"
    )

print(
        f"Cutting Length   : "
        f"{stirrup.cutting_length:.3f} m"
    )


# def clear_screen():
#     # 'nt' artinya Windows, selain itu (seperti 'posix') adalah Mac atau Linux
#     subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

# print("Ini teks lama yang banyak...")
# clear_screen()  # Teks di atas akan hilang dari layar terminal
# print("Sekarang layar sudah bersih!")

print("=" * 55)
print("CONCRETE")
print(parameters.concrete.name, parameters.concrete.fc, "MPa")

print()

print("REINFORCEMENT")
print(parameters.reinforcement.name, parameters.reinforcement.fy, "MPa")

print()

print("BEAM COVER:", parameters.beam_cover, "mm")


from calculation.flexure import calculate_required_rebar

result = calculate_required_rebar(
    Mu=250,  # kN.m, contoh nilai
    beam=beam,
    parameters=parameters,
    bar_diameter=19,
    stirrup_diameter=10
)

print("\n=== BEAM FLEXURAL DESIGN ===")

for key, value in result.items():
    print(f"{key}: {value:.2f}")


from calculation.flexure import calculate_minimum_rebar

minimum_result = calculate_minimum_rebar(
    beam=beam,
    parameters=parameters,
    bar_diameter=19,
    stirrup_diameter=10
)

print("\n=== MINIMUM FLEXURAL REINFORCEMENT ===")

for key, value in minimum_result.items():
    print(f"{key}: {value:.2f}")


from calculation.flexure import select_main_rebar

As_required = result["As_required_mm2"]
As_min = minimum_result["As_min_mm2"]

As_design = max(As_required, As_min)

selected_rebar = select_main_rebar(
    As_design=As_design
)

print("\n=== REBAR SELECTION ===")
print(f"As required       : {As_required:.2f} mm2")
print(f"As minimum        : {As_min:.2f} mm2")
print(f"As design         : {As_design:.2f} mm2")
print(
    f"Selected rebar    : "
    f"{selected_rebar['number_of_bars']}D"
    f"{selected_rebar['diameter_mm']}"
)
print(
    f"As provided       : "
    f"{selected_rebar['As_provided_mm2']:.2f} mm2"
)


from calculation.flexure import check_main_rebar_fit

fit_result = check_main_rebar_fit(
    beam=beam,
    number_of_bars=selected_rebar["number_of_bars"],
    bar_diameter=selected_rebar["diameter_mm"],
    stirrup_diameter=10,
    min_clear_spacing=25
)

print("\n=== MAIN REBAR FIT CHECK ===")

for key, value in fit_result.items():
    print(f"{key}: {value}")


print("-" * 55)


from calculation.rebar_layout import (
    arrange_layers,
    calculate_capacity,
)

layers = arrange_layers(
    beam=beam,
    total_bars=8,
    diameter=22,
    stirrup_diameter=10,
    min_clear_spacing=25,
    min_vertical_clear_spacing=25,
    max_layers=4,
)

result = calculate_capacity(
    beam=beam,
    layers=layers,
    parameters=parameters,
)

Mu = 250  # kN.m, contoh saja

print("\n=== REBAR LAYOUT ===")

for index, layer in enumerate(result["layers"], start=1):
    print(
        f"Layer {index}: "
        f"{layer['quantity']}D{layer['diameter_mm']}, "
        f"y = {layer['y_from_bottom_mm']:.1f} mm, "
        f"As = {layer['area_mm2']:.1f} mm2"
    )

print("\n=== FLEXURAL CAPACITY ===")
print(f"Neutral axis : {result['neutral_axis_mm']:.2f} mm")
print(f"Mn           : {result['Mn_kNm']:.2f} kN.m")
print(f"phi          : {result['phi']:.3f}")
print(f"phi Mn       : {result['phi_Mn_kNm']:.2f} kN.m")
print(f"Mu            : {Mu:.2f} kN.m")

print(
    "Capacity check:",
    "PASS" if result["phi_Mn_kNm"] >= Mu else "FAIL"
)


print("-" * 55)


from calculation.main_rebar import calculate_main_rebar_weight

# Contoh panjang potong per batang.
# Ganti dengan panjang hasil perhitungan detailing-mu.
cutting_length_mm = 6000

weight_result = calculate_main_rebar_weight(
    diameter=selected_rebar["diameter_mm"],
    number_of_bars=selected_rebar["number_of_bars"],
    cutting_length_mm=cutting_length_mm,
)

print("\n=== MAIN REBAR BOQ ===")

for key, value in weight_result.items():
    if isinstance(value, (int, float)):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value}")


print()
print("-" * 55)

print("Beam width:", beam.width)
print("Beam height:", beam.height)

rebar = beam.main_rebars[0]
stirrup = beam.stirrups[0]

print("MainRebar width:", rebar.beam_width)
print("MainRebar height:", rebar.beam_height)

print("Stirrup width:", stirrup.beam_width)
print("Stirrup height:", stirrup.beam_height)

# Contoh: balok panjang 6.000 mm
# Nilai penyaluran berikut hanya untuk menguji program,
# bukan nilai detailing final.

# main_bar = beam.add_main_rebar(
#     mark="B1",
#     diameter=19,
#     quantity=4,
#     anchorage_left=400,
#     anchorage_right=400,
#     position="BOTTOM",
# )

# print("\n=== MAIN REBAR CUTTING LIST ===")
# print(f"Mark              : {main_bar.mark}")
# print(f"Position          : {main_bar.position}")
# print(f"Diameter          : D{main_bar.diameter}")
# print(f"Quantity          : {main_bar.quantity}")
# print(f"Cutting length    : {main_bar.cutting_length_mm:.0f} mm")
# print(f"Total length      : {main_bar.total_length:.2f} m")
# print(f"Unit weight       : {main_bar.unit_weight:.3f} kg/m")
# print(f"Total weight      : {main_bar.total_weight:.2f} kg")
from calculation.beam import Beam
from data.beam_data import BEAM_DATA


def create_beam(beam_type, parameters):
    data = BEAM_DATA[beam_type]

    return Beam(
        name=beam_type,
        width=data["width"],
        height=data["height"],
        length=data["length"],
        parameters=parameters,
    )


from data.beam_design_data import BEAM_DESIGN_DATA

for item in BEAM_DESIGN_DATA:
    beam = create_beam(
        item["beam_type"],
        parameters,
    )

beam = create_beam("B1", parameters)
print("\n=== BEAM DETAILS ===")
print(beam.name)
print(beam.width)
print(beam.height)
print(beam.length)

print()
print(
        beam.name,
        beam.width,
        beam.height,
        item["mark"],
        item["mu"],
        item["vu"],
    )

from data.beam_data import BEAM_DATA
from data.beam_design_data import BEAM_DESIGN_DATA
from calculation.beam_registry import BeamRegistry

registry = BeamRegistry(
    beam_data=BEAM_DATA,
    beam_design_data=BEAM_DESIGN_DATA,
    parameters=parameters,
)

for beam_type, beam in registry.beams.items():
    print(
        beam_type,
        beam.width,
        beam.height,
        beam.length,
    )

for case in registry.get_design_cases():
    print(
        case.beam_type,
        case.beam.width,
        case.beam.height,
        case.mark,
        case.mu,
        case.vu,
    )


print("Jumlah Beam:", len(registry.beams))
print("Jumlah Design Case:", len(registry.design_cases))

for case in registry.get_design_cases():
    print(
        case.beam_type,
        case.mark,
        case.mu,
        case.vu,
    )


from calculation.beam_design_engine import BeamDesignEngine

design_engine = BeamDesignEngine(registry)

design_results = design_engine.initialize_results()


from calculation.design_workflow import design_flexural_case

for case, result in zip(
    registry.get_design_cases(),
    design_results,
):
    design_flexural_case(
        design_case=case,
        result=result,
        fc=40,
        fy=420,
        phi=0.90,
        stirrup_diameter=10,
        main_bar_diameter=19,
        max_bars=8,
    )


print("\nBEAM DESIGN RESULTS")
print("-" * 80)

for result in design_results:
    print(
        f"{result.beam_type:<8}"
        f"{result.beam.width:>8}"
        f"{result.beam.height:>8} "
        f"{result.mark:<22}"
        f"{result.mu:>12}"
        f"{result.vu:>12}"
        f"{result.status:>18}"
    )

print("-" * 80)
print("Total Design Case:", len(design_results))


# result = calculate_required_rebar(
#     design_case=case,
#     parameters=parameters,
# )

from calculation.flexural_design import (
    calculate_required_rebar,
)

case = registry.get_design_cases("B1")[0]

result = calculate_required_rebar(
    design_case=case,
    fc=40,
    fy=420,
    phi=0.90,  # nilai ilustrasi, bukan final
    stirrup_diameter=10,
    main_bar_diameter=19,
)

print("\nFLEXURAL DESIGN")
print("-" * 50)

for key, value in result.items():
    print(f"{key:<20}: {value}")

print("-" * 50)
from calculation.bar_selection import select_main_rebar

# result = select_main_rebar(
#     as_required=2000,  # mm2, contoh nilai
#     diameter=22,
#     max_bars=8,
# )

# print(result)

print("-" * 50)
print("\nFLEXURAL DESIGN SUMMARY")
print("-" * 100)

for result in design_results:
    print(
        f"{result.beam_type:<6}"
        f"{result.mark:<22}"
        f"{result.mu:>10.1f}"
        f"{result.as_required:>12.1f}"
        f"{result.main_bar_quantity:>8}"
        f"D{result.main_bar_diameter:<6}"
        f"{result.as_provided:>12.1f}"
    )

print("-" * 50)


print(
    f"{'TYPE':<8}"
    f"{'MARK':<20}"
    f"{'Mu':>10}"
    f"{'QTY':>8}"
    f"{'BAR':<7}"
    f"{'As_req':>12}"
    f"{'As_prov':>12}"
    f"{'phiMn':>12}"
    f"{'STATUS':>20}"
)

print("-" * 109)


for case, result in zip(
    registry.get_design_cases(),
    design_results,
):
    result, check = design_flexural_case(
        design_case=case,
        result=result,
        fc=40,
        fy=420,
        phi=0.90,
        stirrup_diameter=10,
        main_bar_diameter=19,
        max_bars=8,
    )
    
    

    print(
        f"{case.beam_type:<8}"
        f"{case.mark:<20}"
        f"{case.mu:>10.2f}"
        f"{result.main_bar_quantity:>8}"
        f"D{result.main_bar_diameter:<6}"
        f"{result.as_required:>12.2f}"
        f"{result.as_provided:>12.2f}"
        f"{check['phi_Mn_kNm']:>12.2f}"
        f"{check['status']:>20}"
    )
