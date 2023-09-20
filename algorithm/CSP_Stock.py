from ortools.sat.python import cp_model

from . import CSP_Base


class CSP_Stock(CSP_Base):
    def __init__(self, opt):
        super().__init__(opt)
        self.stocks = opt.stocks

    def set_objective(self):
        self.model.Minimize(
            cp_model.LinearExpr.Sum([self.reel_var[j] for j in self.data["reels"]])
        )

    def optimize(self, orders):
        super().optimize(orders)

        if self.status == cp_model.OPTIMAL or self.status == cp_model.FEASIBLE:
            result = self.extract_solution()
            return result
        else:
            return []

    def predict_reels(self):
        SAFETY_FACTOR = 10
        OVER_ESTIMATION_RATIO = 1.2

        order_total = sum(self.orders["width"] * self.orders["quantity"])
        predict_reels = (
            order_total // self.bin_capacity["lb"]
        ) * OVER_ESTIMATION_RATIO + SAFETY_FACTOR
        return predict_reels

    def get_data(self):
        super().get_data()
        self.data.update(
            {
                "stocks": self.stocks.to_dict("records"),
                "stock_items": list(range(len(self.stocks))),
            }
        )

    def create_variables(self):
        super().create_variables()

        self.stock_var = {}
        for stock in self.data["stock_items"]:
            for reel in self.data["reels"]:
                self.stock_var[(stock, reel)] = self.model.NewIntVar(
                    0, self.MAX_VARIABLE_INT, f"stock_var[{stock},{reel}]"
                )

    def add_constraints(self):
        super().add_constraints()
        for j in self.data["reels"][1:]:
            self.model.Add(self.reel_var[j - 1] >= self.reel_var[j])

        for order in self.data["order_items"]:
            order_qty = self.data["orders"][order]["quantity"]
            self.model.Add(
                sum(self.order_var[order, reel] for reel in self.data["reels"])
                == order_qty
            )

        MAX_ORDER_QTY = 5
        for reel in self.data["reels"]:
            total_order_qty = sum(
                self.order_var[(order, reel)] for order in self.data["order_items"]
            )
            total_stock_qty = sum(
                self.stock_var[(stock, reel)] for stock in self.data["stock_items"]
            )
            self.model.Add(total_order_qty + total_stock_qty <= MAX_ORDER_QTY)

            total_order_width = sum(
                self.order_var[(order, reel)] * self.data["orders"][order]["width"]
                for order in self.data["order_items"]
            )
            total_stock_width = sum(
                self.stock_var[(stock, reel)] * self.data["stocks"][stock][self.unit]
                for stock in self.data["stock_items"]
            )
            self.model.Add(
                (total_order_width + total_stock_width)
                <= self.reel_var[reel] * self.bin_capacity["ub"]
            )
            self.model.Add(
                (total_order_width + total_stock_width)
                >= self.reel_var[reel] * self.bin_capacity["lb"]
            )

    def extract_solution(self):
        result = []
        packed_df = self.orders.copy()
        packed_df["quantity"] = 0

        for reel in self.data["reels"]:  # Check the status of the reels number.
            if self.solver.Value(self.reel_var[reel]) != 1:
                continue

            packed_orders, packed_stocks = [], []  # record

            for order in self.data["order_items"]:
                qty = self.solver.Value(self.order_var[order, reel])
                packed_orders.extend(
                    [self.data["orders"][order]["width"] / self.magnification]
                    * int(qty)
                )
                packed_df.loc[order, "quantity"] += qty  # record

            for stock in self.data["stock_items"]:
                qty = self.solver.Value(self.stock_var[stock, reel])
                packed_stocks.extend(
                    [self.data["stocks"][stock][self.opt.unit] / self.opt.magnification]
                    * int(qty)
                )

            total_packs = packed_orders + packed_stocks

            # fmt: off
            _schedule = {
                "base_wei": self.opt.base_wei,
                "width1": None,"width2": None, "width3": None, 
                "width4": None, "width5": None,
                "unit": self.unit, "total": sum(total_packs), "quantity": 1,
                "remark": f"stock:{packed_stocks}" if packed_stocks else "",
            }
            # fmt: on
            for idx, pack in enumerate(sorted(total_packs, reverse=True), start=1):
                _schedule[f"width{idx}"] = pack

            result.append(_schedule)

        self.orders["quantity"] -= packed_df["quantity"]

        return result
