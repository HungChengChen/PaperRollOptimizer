import datetime
import os


class Logger(object):
    def __init__(self, opt):
        self.opt = opt
        # 記錄起始時間
        self.start_time = datetime.datetime.now()
        self.init_log_dir()
        self.log_file = self.create_log_file()
        self.write_options_to_file()

    def init_log_dir(self):
        # 創建儲存目錄
        if not os.path.exists(self.opt.save_dir):
            os.makedirs(self.opt.save_dir)

        time_str = self.start_time.strftime("%Y-%m-%d-%H-%M-%S")  # 時間轉為字串格式
        self.log_dir = os.path.join(self.opt.save_dir, f"logs_{time_str}")  # 日誌目錄路徑
        self.opt.log_dir = self.log_dir
        os.makedirs(self.log_dir, exist_ok=True)

    def create_log_file(self):
        # 創建並開啟日誌文件
        log_file_path = os.path.join(self.log_dir, "log.txt")
        return open(log_file_path, "w", encoding="utf-8")

    def write_options_to_file(self):
        # 寫入選項到文件
        args = vars(self.opt)
        file_path = os.path.join(self.log_dir, "opt.txt")
        with open(file_path, "wt", encoding="utf-8") as opt_file:
            opt_file.write("==> Opt:\n")
            for k, v in sorted(args.items()):
                opt_file.write(f"  {k}: {v}\n")

    def write(self, txt):
        # 計算並寫入執行時間
        print(txt)
        elapsed_time = (
            datetime.datetime.now() - self.start_time
        ).total_seconds()  # Now it works
        message = f"({elapsed_time}s) {txt}\n"
        self.log_file.write(message)

    def close(self):
        # 關閉日誌文件
        self.log_file.close()
