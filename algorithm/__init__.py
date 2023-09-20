from ortools.sat.python import cp_model


class CSP_Base:
    def __init__(self, opt):
        self.opt = opt
        self.cpu = opt.cpu
        self.unit = opt.unit
        self.max_time = opt.max_time
        self.bin_capacity = opt.bin_capacity
        self.magnification = opt.magnification

    # 啟動最佳化流程的方法
    def optimize(self, orders):
        # 過濾訂單數量大於0的訂單並重設索引
        self.orders = orders[orders["quantity"] > 0].reset_index(drop=True)

        # 創建一個約束模型
        self.model = cp_model.CpModel()

        # 流程
        self.get_data()  # 獲取數據
        self.create_variables()  # 創建變量
        self.add_constraints()  # 添加約束
        self.set_objective()  # 設定目標

        # 創建一個求解器並設置參數
        self.solver = cp_model.CpSolver()
        self.solver.parameters.num_search_workers = self.opt.cpu
        self.solver.parameters.max_time_in_seconds = self.max_time
        printer = cp_model.ObjectiveSolutionPrinter()
        # 求解並返回狀態
        self.status = self.solver.Solve(self.model, printer)

        # if self.status == cp_model.OPTIMAL or self.status == cp_model.FEASIBLE:
        #     result = self.extract_solution()
        #     return result
        # else:
        #     return []

    # 設置目標函數的方法（需要在子類中實現）
    def set_objective(self):
        return NotImplementedError

    # 預測輸出的方法（需要在子類中實現）
    def predict_reels(self):
        return NotImplementedError

    # 處理並獲取數據的方法
    def get_data(self):
        print("predict_reels :", int(self.predict_reels()))
        self.data = {
            "orders": self.orders.to_dict("records"),
            "order_items": list(range(len(self.orders))),
            "reels": list(range(int(self.predict_reels()))),
        }

    # 創建變數
    def create_variables(self):
        self.MAX_VARIABLE_INT = 5
        self.order_var = {}
        for order in self.data["order_items"]:
            for reel in self.data["reels"]:
                self.order_var[(order, reel)] = self.model.NewIntVar(
                    0, self.MAX_VARIABLE_INT, f"order_var[{order},{reel}]"
                )

        self.reel_var = {}
        for reel in self.data["reels"]:
            self.reel_var[reel] = self.model.NewBoolVar(f"reel_var[{reel}]")

    # 添加約束的方法（需要在子類中實現）
    def add_constraints(self):
        return NotImplementedError
