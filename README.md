# FinBuddy - A股金融情报助手

[English](README_EN.md) | [繁體中文](README_TC.md)

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="Version">
</p>

<p align="center">
  🎯 <strong>基于LLM的A股上市公司公告解读、市场情绪分析与财务数据智能分析工具</strong>
</p>

---

## 🎉 项目介绍

**FinBuddy** 是一款专为A股市场设计的金融情报助手，旨在帮助投资者、分析师和研究人员快速获取、处理和分析上市公司信息。

### 🔥 核心价值

- ⚡ **快速分析**: 数秒内完成公告情绪判断与关键信息提取
- 🧠 **智能解读**: 基于金融词典 + LLM（可选）深度理解
- 📊 **数据驱动**: 量化财务指标，生成专业分析报告
- 🔒 **本地优先**: 零外部依赖，敏感数据不出本地

### ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 📰 **情绪分析** | 分析新闻/公告情绪倾向，判断利好/利空 |
| 📋 **公告摘要** | 自动提取关键点、风险因素、投资信号 |
| 📈 **财务报告** | 生成估值分析报告，支持多格式导出 |
| 🔍 **批量处理** | 支持批量新闻/公告分析，效率翻倍 |

### 🐚 灵感来源

本项目参考了 **Kronos**（金融市场语言基础模型）的设计思路，专注于A股垂直场景，提供开箱即用的中文金融分析能力。

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- rich >= 13.0.0（用于美化终端输出）
- requests >= 2.28.0（用于HTTP请求）
- 可选: openai >= 1.0.0 或 anthropic >= 0.20.0（启用LLM深度分析）

### 📦 安装

```bash
# 从源码安装（推荐）
git clone https://github.com/gitstq/finbuddy.git
cd finbuddy
pip install -e .

# 或者直接安装
pip install .
```

### 💡 快速使用

#### 1. 情绪分析

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 分析单条文本
result = analyzer.analyze_text("某公司业绩大幅增长，净利润同比增长50%")
print(f"情绪: {result.level.value}, 分数: {result.score:.3f}")
# 输出: 情绪: 偏乐观, 分数: 0.650
```

#### 2. 公告摘要

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

summary = summarizer.parse_announcement(
    text="预计2024年净利润增长20%，决定进行股票回购",
    title="2024年度业绩预告",
    publish_date="2025-01-15"
)

print(f"类型: {summary.announcement_type}")
print(f"信号: {summary.investment_signal}")
# 输出: 类型: 业绩预告, 信号: 利好
```

#### 3. 财务报告

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

report = reporter.create_report(
    stock_code="600519",
    company_name="贵州茅台",
    financial_data={
        "revenue": 1500,
        "profit": 750,
        "eps": 60.0,
        "roe": 30.5,
        "pe": 35.0,
    }
)

# 终端格式输出
print(reporter.format_terminal(report))

# JSON格式输出
print(reporter.format_json(report))

# Markdown格式输出
print(reporter.format_markdown(report))
```

#### 4. 命令行工具

```bash
# 情绪分析
finbuddy sentiment --text "某公司业绩大幅增长"

# 批量情绪分析
finbuddy batch-sentiment --file news.txt

# 公告摘要
finbuddy announce --file announcement.txt --title "业绩预告"

# 财务报告
finbuddy financial --code 600519 --name "贵州茅台" \
    --data '{"revenue":1500,"profit":750,"eps":60}'

# 综合分析
finbuddy analyze --code 600519 --name "贵州茅台" \
    --news-file news.txt --fin-file financial.json
```

---

## 📖 详细使用指南

### 情绪分析 API

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 单条分析
result = analyzer.analyze_text("市场情绪积极")

# 批量分析
results = analyzer.analyze_batch([
    "利好消息",
    "利空消息",
    "市场平稳"
])

# 市场情绪指数
sentiment = analyzer.get_market_sentiment([
    {"title": "新闻1", "content": "业绩增长"},
    {"title": "新闻2", "content": "订单大增"}
])
```

### 公告摘要 API

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

# 解析公告
summary = summarizer.parse_announcement(
    text="公告全文...",
    title="公告标题",
    publish_date="2025-01-15"
)

# 批量解析
summaries = summarizer.parse_batch([
    {"text": "...", "title": "业绩预告"},
    {"text": "...", "title": "分红公告"}
])

# 按信号过滤
bullish = summarizer.filter_by_signal(summaries, "利好")
```

### 财务报告 API

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

# 创建报告
report = reporter.create_report(
    stock_code="600519",
    company_name="贵州茅台",
    financial_data={
        "revenue": 1500,      # 营业收入（亿元）
        "profit": 750,       # 净利润（亿元）
        "eps": 60.0,         # 每股收益（元）
        "roe": 30.5,         # 净资产收益率（%）
        "pe": 35.0,          # 市盈率
        "pb": 12.0,          # 市净率
    }
)

# 输出格式
print(report.format_terminal())  # 终端格式
print(report.format_json())       # JSON格式
print(report.format_markdown())   # Markdown格式
```

### FinBuddyClient 整合客户端

```python
from finbuddy import FinBuddyClient
from finbuddy.client import StockInfo

client = FinBuddyClient()

# 综合分析
result = client.comprehensive_analysis(
    stock=StockInfo(
        code="600519",
        name="贵州茅台",
        market="SH",
        industry="白酒",
        sector="消费"
    ),
    news=["业绩增长", "新品上市"],
    announcements=[{"text": "...", "title": "业绩预告"}],
    financial_data={"revenue": 1500, "profit": 750}
)

print(f"整体信号: {result.overall_signal}")
```

---

## 💡 设计思路

### 技术选型

- **Python 3.8+**: 广泛兼容，数据科学生态丰富
- **Rich**: 终端美化，提升可读性
- **无LLM依赖**: 基础功能基于词典，无需API Key
- **可选LLM**: 支持接入OpenAI/Anthropic进行深度分析

### 架构设计

```
finbuddy/
├── analyzer.py      # 情绪分析模块
├── summarizer.py    # 公告摘要模块
├── reporter.py      # 财务报告模块
├── client.py        # 整合客户端
└── cli.py           # 命令行工具
```

### 后续迭代

- [ ] 支持更多数据源接入（东方财富、同花顺等）
- [ ] 添加技术面分析模块（K线形态、均线系统）
- [ ] 支持更多LLM后端（Claude、Gemini、文心一言等）
- [ ] Web界面和API服务
- [ ] 支持港股、美股分析

---

## 📦 打包与部署

### 构建安装包

```bash
# 构建wheel包
python -m build

# 构建源码包
python -m build --sdist
```

### 依赖安装

```bash
# 仅核心依赖
pip install finbuddy

# 包含LLM支持
pip install finbuddy[llm]

# 开发依赖
pip install finbuddy[dev]

# 全部依赖
pip install finbuddy[all]
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目采用 MIT 开源协议，详情请参阅 [LICENSE](LICENSE) 文件。

---

<p align="center">
  ⭐ 如果这个项目对您有帮助，请给我们一个 Star！
</p>

<p align="center">
  © 2026 FinBuddy | MIT License
</p>
