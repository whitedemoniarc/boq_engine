from reports.report_utils import (
    print_section,
    print_separator,
)


def print_flexural_report(results):
    print_section("2. Beam Flexural Design")

    headers = (
        f"{'TYPE':<8}"
        f"{'MARK':<18}"
        f"{'POS':<8}"
        f"{'B_mm':>8}"
        f"{'H_mm':>8}"
        f"{'Mu_kNm':>12}"
        f"{'QTYBAR':>10}"
        f"{'As_req':>12}"
        f"{'As_prov':>12}"
        f"{'phiMn':>12}"
        f"{'Margin':>12}"
        f"{'STATUS':>20}"
    )

    print(headers)
    print_separator(len(headers))

    for result in results:
        print(
            f"{result.beam_type:<8}"
            f"{result.mark:<18}"
            f"{result.position:<8}"
            f"{result.width:>8}"
            f"{result.height:>8}"
            f"{result.mu_kNm:>12.2f}"
            f"{result.qtybar:>10}"
            f"{result.as_required:>12.2f}"
            f"{result.as_provided:>12.2f}"
            f"{result.phi_Mn_kNm:>12.2f}"
            f"{result.margin:>12.2f}"
            f"{result.status:>20}"
        )
