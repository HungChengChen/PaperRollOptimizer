from ortools.sat.python import cp_model

from algorithm.CSP_Stock import CSP_Stock
from logger import Logger
from opt import opts
from utils import solution_printer


def main():
    opt = opts().parse()
    logger = Logger(opt)
    opt.logger = logger

    solution = []
    remaining_order = opt.orders

    SUCCESS_STAT = [cp_model.OPTIMAL, cp_model.FEASIBLE]
    csp_stock = CSP_Stock(opt)
    result = csp_stock.optimize(remaining_order)  # 執行優化
    # 確認是否有解
    if csp_stock.status in SUCCESS_STAT and result:
        solution.extend(result)
        remaining_order = csp_stock.orders
        APS_json = solution_printer(result, opt)


if __name__ == "__main__":
    main()
