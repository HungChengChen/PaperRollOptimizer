# 🌀 PaperRoll_Optimizer

<p align="center">
  <img src="doc/image/so31dk0x.png" alt="" width="50%">
  <br>
  <i>智能化造紙生產流程(Image generated using DALL·E-3 by OpenAI.)</i>
</p>

## 🌟 簡介

**PaperRoll_Optimizer** 是為造紙廠量身打造的 Cutting Stock Problem (CSP) 解決方案。此工具致力於從固定尺寸的紙卷中最大化裁剪效率，同時確保符合客戶的訂單需求。

在造紙廠的日常運營中，如何從原料紙漿製作固定尺寸的大捲筒，並根據訂單需求精確裁剪，始終是一大挑戰。`PaperRoll_Optimizer` 旨在解決此問題，確保每次裁剪都能最大化資源利用並最小化浪費。

## 📘 背景

- 🌲 **原料處理:** 我們首先將原料紙漿轉化成`129英吋`的大捲筒。
- 📏 **訂單複卷:** 精確地根據客戶的需求進行複卷操作。
- ⚙️ **機器限制:** 儘管一卷大捲筒的上限為`5`卷，但我們確保每次切割都達到最佳效果，餘料不超過`1英吋`。
- 🗃️ **庫存填充:** 通過智能系統從庫存中選擇適當的紙卷進行填充，確保總寬度介於`128~129英吋`之間。

## ✨ 主要特點

- 📏 **訂單優化**：組合訂單，目的是減少成本、浪費和庫存。
- 🌀 **複卷機適應性**：確保一卷大捲筒的最大切割量為`5卷`。
- 📦 **餘料策略**：確保餘料最小，不足部分則由庫存紙卷補充。
- 🏭 **庫存平衡**：自動設定和平衡各庫存尺寸的數量，以避免單一庫存尺寸過多。
- 🧩 **模組化開發**：方便維護和擴展，使新增功能更為便捷。
- 📊 助力造紙廠提高生產效率。
- 🔍 使用 `OR-Tools` 進行線性規劃，快速找到最佳裁剪策略。
- 🖥️ `OR-Tools`：簡單安裝、使用方便，且完全開源。

## 📥 安裝

**安裝依賴**:

```bash
pip install pandas ortools argparse
```

## 📖 使用範例

在使用前，您可以透過以下檔案進行設定：

- `machine_specs.json`：設定機台的寬幅規格。
- `order.xlsx`：設定訂單的英寸寬幅數量。
- `stocks_width.xlsx`：設定庫存的英寸寬幅。
- `cpu`：設定 CPU 核心數量(默認為 8)。
- `max_time`：設定解決問題的時間限制(秒數，默認為 30 秒)。

執行範例：

```bash
python main.py --cpu 4 --max_time 60
```

## 🖼️ 優化結果展示

```markdown
> Bin capacity: {'lb': 128, 'ub': 129}
> predict_reels : 24
> Solution 0, time = 0.62 s, objective = 13
> APS:
> base_wei width1 width2 width3 width4 width5 unit total remark quantity
> 0 NaN 43.0 43.0 43.0 NaN NaN inch 129.0 1
> 1 NaN 43.0 36.0 25.0 25.0 NaN inch 129.0 1
> 2 NaN 43.0 34.0 27.0 25.0 NaN inch 129.0 1
> 3 NaN 36.0 36.0 32.0 25.0 NaN inch 129.0 2
> 4 NaN 36.0 34.0 34.0 25.0 NaN inch 129.0 1
> 5 NaN 36.0 31.0 31.0 31.0 NaN inch 129.0 3
> 6 NaN 34.0 34.0 34.0 26.0 NaN inch 128.0 stock:[26.0] 1
> 7 NaN 32.0 32.0 32.0 32.0 NaN inch 128.0 1
> 8 NaN 27.0 27.0 27.0 27.0 21.0 inch 129.0 stock:[21.0] 1
> 9 NaN 27.0 27.0 25.0 25.0 25.0 inch 129.0 stock:[25.0] 1

> APS to json format...
```

## ⚠️ 目前版本注意事項

目前本版關閉以下功能，僅供教學參考使用：

- 選擇機台功能
- 選擇單位功能
- 建立多樣的庫存尺吋表
- 介面顯示
- 顯示基重等欄位資訊
- 更強大的演算法，用於快速解決大量訂單

如有任何問題或需要這些功能，請聯絡開發者。

## 👤 開發者聯絡方式

- 開發者：hungcheng.chen
- 電子郵件：[hungcheng.chen@outlook.com](mailto:hungcheng.chen@outlook.com)
