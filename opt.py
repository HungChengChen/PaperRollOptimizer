import argparse
import json
import os

import pandas as pd


class opts(object):
    def __init__(self):
        self.opt = None

        # fmt: off
        # 初始化一個argparse.ArgumentParser物件，用於處理命令行參數
        self.parser = argparse.ArgumentParser()
        # self.parser.add_argument("--machine", type=int, help="選擇使用的機器(1 或 2)")
        # self.parser.add_argument("--unit", type=str, help="選擇單位 (台尺, inch, cm, mm)")
        self.parser.add_argument("--cpu", default=8, type=int, help="設定 CPU 核心數量(默認為 8)")
        self.parser.add_argument("--max_time", default=30, type=int, help="設定解決問題的時間限制(秒數，默認為 30 秒)")
        # self.parser.add_argument("--magnification", default=100, type=int, help="設定倍率(默認為 100)")
        # fmt: on

    # def parse(self, orders, args=""):
    def parse(self, args=""):
        # step 1 : 解析命令行參數
        self.opt = self.parser.parse_args(args if args else [])
        # 設定根路徑和保存目錄
        self.opt.root = os.path.dirname(os.path.abspath(__file__))
        # self.opt.save_dir = os.path.join(
        #     self.opt.root, "results", f"{self.opt.machine}_{self.opt.unit}"
        # )
        self.opt.unit = "inch"
        self.opt.save_dir = os.path.join(self.opt.root, "results", f"{self.opt.unit}")
        self.opt.magnification = 1  # 倍率設定為 100
        # step 2 : 設定機器規格和總寬幅上下限
        self.load_machine_specs()  # 讀取機器規格
        self.set_bin_capacity()  # 設定容器容量

        # 數據處理
        self.preparing_order_data()  # 訂單
        self.preparing_stock_data()  # 根據機器選擇庫存

        return self.opt

    # 從 ./data 中讀取機器規格json 文件
    def load_machine_specs(self):
        with open(
            os.path.join(self.opt.root, "data", "machine_specs.json"), encoding="utf-8"
        ) as f:
            self.machine_specs = json.load(f)

    def set_bin_capacity(self):
        # 如果機器選擇或單位輸入錯誤，則引發錯誤
        # fmt: off
        # if str(self.opt.machine) not in self.machine_specs:
        #     raise ValueError("Incorrect machine selection, please choose machine 1 or 2")

        # if self.opt.unit not in self.machine_specs[str(self.opt.machine)]:
        #     raise ValueError("Incorrect unit input, please enter a correct unit (Taiwanese foot, inch, cm, mm)")
        # fmt: on

        # 設定容器容量，
        # capacity = self.machine_specs[str(self.opt.machine)][self.opt.unit]
        capacity = self.machine_specs[self.opt.unit]
        self.opt.bin_capacity = {
            "lb": int(capacity["lb"] * self.opt.magnification),
            "ub": int(capacity["ub"] * self.opt.magnification),
        }
        print("Bin capacity: ", self.opt.bin_capacity)

    # def get_base_wei(self, orders):
    #     self.opt.base_wei = orders["base_wei"][0]

    def preparing_order_data(self):
        # 準備訂單數據：按寬度分組並求和，並按照倍率將寬度轉換為整數
        order_path = os.path.join(self.opt.root, "data", f"order.xlsx")
        orders = pd.read_excel(order_path, usecols=["width", "quantity"])
        # orders = pd.DataFrame.from_records(orders)
        # self.get_base_wei(orders)  # 獲取基重
        # self.opt.base_wei = orders["base_wei"][0]
        self.opt.base_wei = None

        orders = orders.groupby("width").quantity.sum().reset_index()
        orders["width"] = (orders["width"] * self.opt.magnification).astype(int)
        self.opt.orders = orders

    def preparing_stock_data(self):
        # 準備庫存數據：從 excel 讀取數據，並按照倍率將單位列轉換為整數
        stock_path = os.path.join(self.opt.root, "data", f"stocks_width.xlsx")

        stocks = pd.read_excel(stock_path, usecols=[self.opt.unit, "Quantity"])
        stocks[self.opt.unit] = (stocks[self.opt.unit] * self.opt.magnification).astype(
            int
        )
        self.opt.stocks = stocks
