# FinBuddy - A股金融情報助手

[English](README_EN.md) | 简体中文

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="Version">
</p>

<p align="center">
  🎯 <strong>基於LLM的A股上市公司公告解讀、市場情緒分析與財務數據智慧分析工具</strong>
</p>

---

## 🎉 專案介紹

**FinBuddy** 是一款專為A股市場設計的金融情報助手，旨在幫助投資者、分析師和研究人員快速獲取、處理和分析上市公司資訊。

### 🔥 核心價值

- ⚡ **快速分析**: 數秒內完成公告情緒判斷與關鍵資訊提取
- 🧠 **智慧解讀**: 基於金融詞典 + LLM（可選）深度理解
- 📊 **數據驅動**: 量化財務指標，生成專業分析報告
- 🔒 **本地優先**: 零外部依賴，敏感數據不出本地

### ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📰 **情緒分析** | 分析新聞/公告情緒傾向，判斷利好/利空 |
| 📋 **公告摘要** | 自動提取關鍵點、風險因素、投資信號 |
| 📈 **財務報告** | 生成估值分析報告，支援多格式導出 |
| 🔍 **批量處理** | 支援批量新聞/公告分析，效率翻倍 |

### 🐚 靈感來源

本專案參考了 **Kronos**（金融市場語言基礎模型）的設計思路，專注於A股垂直場景，提供開箱即用的中文金融分析能力。

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- rich >= 13.0.0（用於美化終端輸出）
- requests >= 2.28.0（用於HTTP請求）
- 可選: openai >= 1.0.0 或 anthropic >= 0.20.0（啟用LLM深度分析）

### 📦 安裝

```bash
# 從源碼安裝（推薦）
git clone https://github.com/gitstq/finbuddy.git
cd finbuddy
pip install -e .

# 或者直接安裝
pip install .
```

### 💡 快速使用

#### 1. 情緒分析

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 分析單條文本
result = analyzer.analyze_text("某公司業績大幅增長，淨利潤同比增長50%")
print(f"情緒: {result.level.value}, 分數: {result.score:.3f}")
# 輸出: 情緒: 偏樂觀, 分數: 0.650
```

#### 2. 公告摘要

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

summary = summarizer.parse_announcement(
    text="預計2024年淨利潤增長20%，公司決定進行股票回購",
    title="2024年度業績預告",
    publish_date="2025-01-15"
)

print(f"類型: {summary.announcement_type}")
print(f"信號: {summary.investment_signal}")
# 輸出: 類型: 業績預告, 信號: 利好
```

#### 3. 財務報告

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

report = reporter.create_report(
    stock_code="600519",
    company_name="貴州茅臺",
    financial_data={
        "revenue": 1500,
        "profit": 750,
        "eps": 60.0,
        "roe": 30.5,
        "pe": 35.0,
    }
)

# 終端格式輸出
print(reporter.format_terminal(report))

# JSON格式輸出
print(reporter.format_json(report))

# Markdown格式輸出
print(reporter.format_markdown(report))
```

#### 4. 命令列工具

```bash
# 情緒分析
finbuddy sentiment --text "某公司業績大幅增長"

# 批量情緒分析
finbuddy batch-sentiment --file news.txt

# 公告摘要
finbuddy announce --file announcement.txt --title "業績預告"

# 財務報告
finbuddy financial --code 600519 --name "貴州茅臺" \
    --data '{"revenue":1500,"profit":750,"eps":60}'

# 綜合分析
finbuddy analyze --code 600519 --name "貴州茅臺" \
    --news-file news.txt --fin-file financial.json
```

---

## 📖 詳細使用指南

### 情緒分析 API

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 單條分析
result = analyzer.analyze_text("市場情緒積極")

# 批量分析
results = analyzer.analyze_batch([
    "利好消息",
    "利空消息",
    "市場平穩"
])

# 市場情緒指數
sentiment = analyzer.get_market_sentiment([
    {"title": "新聞1", "content": "業績增長"},
    {"title": "新聞2", "content": "訂單大增"}
])
```

### 公告摘要 API

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

# 解析公告
summary = summarizer.parse_announcement(
    text="公告全文...",
    title="公告標題",
    publish_date="2025-01-15"
)

# 批量解析
summaries = summarizer.parse_batch([
    {"text": "...", "title": "業績預告"},
    {"text": "...", "title": "分紅公告"}
])

# 按信號過濾
bullish = summarizer.filter_by_signal(summaries, "利好")
```

### 財務報告 API

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

# 創建報告
report = reporter.create_report(
    stock_code="600519",
    company_name="貴州茅臺",
    financial_data={
        "revenue": 1500,      # 營業收入（億元）
        "profit": 750,       # 淨利潤（億元）
        "eps": 60.0,         # 每股收益（元）
        "roe": 30.5,         # 淨資產收益率（%）
        "pe": 35.0,          # 市盈率
        "pb": 12.0,          # 市凈率
    }
)

# 輸出格式
print(report.format_terminal())  # 終端格式
print(report.format_json())       # JSON格式
print(report.format_markdown())   # Markdown格式
```

### FinBuddyClient 整合客戶端

```python
from finbuddy import FinBuddyClient
from finbuddy.client import StockInfo

client = FinBuddyClient()

# 綜合分析
result = client.comprehensive_analysis(
    stock=StockInfo(
        code="600519",
        name="貴州茅臺",
        market="SH",
        industry="白酒",
        sector="消費"
    ),
    news=["業績增長", "新品上市"],
    announcements=[{"text": "...", "title": "業績預告"}],
    financial_data={"revenue": 1500, "profit": 750}
)

print(f"整體信號: {result.overall_signal}")
```

---

## 💡 設計思路

### 技術選型

- **Python 3.8+**: 廣泛兼容，數據科學生態豐富
- **Rich**: 終端美化，提升可讀性
- **無LLM依賴**: 基礎功能基於詞典，無需API Key
- **可選LLM**: 支援接入OpenAI/Anthropic進行深度分析

### 架構設計

```
finbuddy/
├── analyzer.py      # 情緒分析模組
├── summarizer.py    # 公告摘要模組
├── reporter.py       # 財務報告模組
├── client.py        # 整合客戶端
└── cli.py           # 命令列工具
```

### 後續迭代

- [ ] 支援更多數據源接入（東方財富、同花順等）
- [ ] 添加技術面分析模組（K線形態、均線系統）
- [ ] 支援更多LLM後端（Claude、Gemini、文心一言等）
- [ ] Web界面和API服務
- [ ] 支援港股、美股分析

---

## 📦 打包與部署

### 構建安裝包

```bash
# 構建wheel包
python -m build

# 構建源碼包
python -m build --sdist
```

### 依賴安裝

```bash
# 僅核心依賴
pip install finbuddy

# 包含LLM支援
pip install finbuddy[llm]

# 開發依賴
pip install finbuddy[dev]

# 全部依賴
pip install finbuddy[all]
```

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

---

## 📄 開源協議

本專案採用 MIT 開源協議，詳情請参阅 [LICENSE](LICENSE) 文件。

---

<p align="center">
  ⭐ 如果這個專案對您有幫助，請給我們一個 Star！
</p>

<p align="center">
  © 2026 FinBuddy | MIT License
</p>
