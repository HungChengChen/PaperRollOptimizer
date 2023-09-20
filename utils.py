import pandas as pd


def solution_printer(solution, opt):
    solution.sort(
        key=lambda x: (x.get("width1"), x.get("width2"), x.get("width3")),
        reverse=True,
    )
    APS = pd.DataFrame(solution)
    # fmt: off
    APS = (
        APS.groupby(
            [
                "base_wei",
                "width1", "width2", "width3", "width4", "width5",
                "unit", "total", "remark",
            ],
            dropna=False,
            sort=False,
        )["quantity"].sum().reset_index()
    )
    # fmt: on
    opt.logger.write(f"APS: \n{APS}" + "\n")
    opt.logger.write(f"APS to json format...")
    # print(APS)
    # print("APS to json format...")
    APS.to_excel(f"{opt.log_dir}/APS.xlsx", index=False)
    # APS.to_excel("data/APS.xlsx", index=False)
    APS_json = APS.to_json(orient="records", indent=4)
    return APS_json
