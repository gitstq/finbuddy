# FinBuddy - A-Share Financial Intelligence Assistant

简体中文 | [繁體中文](README_TC.md)

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Version-1.0.0-orange.svg" alt="Version">
</p>

<p align="center">
  🎯 <strong>LLM-powered A-share stock announcement analysis, market sentiment analysis, and financial data intelligence tool</strong>
</p>

---

## 🎉 Project Introduction

**FinBuddy** is a financial intelligence assistant designed specifically for the A-share (Chinese stock) market, helping investors, analysts, and researchers quickly obtain, process, and analyze listed company information.

### 🔥 Core Values

- ⚡ **Fast Analysis**: Complete announcement sentiment analysis and key information extraction in seconds
- 🧠 **Smart Interpretation**: Based on financial dictionary + LLM (optional) for deep understanding
- 📊 **Data-Driven**: Quantify financial indicators, generate professional analysis reports
- 🔒 **Local-First**: Zero external dependencies, sensitive data stays local

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📰 **Sentiment Analysis** | Analyze news/announcement sentiment, determine bullish/bearish signals |
| 📋 **Announcement Summary** | Auto-extract key points, risk factors, investment signals |
| 📈 **Financial Report** | Generate valuation analysis reports, multi-format export |
| 🔍 **Batch Processing** | Batch news/announcement analysis, doubled efficiency |

### 🐚 Inspiration

This project is inspired by **Kronos** (Financial Market Language Foundation Model), focusing on the A-share vertical scenario, providing out-of-the-box Chinese financial analysis capabilities.

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- rich >= 13.0.0 (for beautiful terminal output)
- requests >= 2.28.0 (for HTTP requests)
- Optional: openai >= 1.0.0 or anthropic >= 0.20.0 (for LLM deep analysis)

### 📦 Installation

```bash
# Install from source (recommended)
git clone https://github.com/gitstq/finbuddy.git
cd finbuddy
pip install -e .

# Or install directly
pip install .
```

### 💡 Quick Usage

#### 1. Sentiment Analysis

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Analyze single text
result = analyzer.analyze_text("Company earnings grew significantly, net profit up 50% YoY")
print(f"Sentiment: {result.level.value}, Score: {result.score:.3f}")
# Output: Sentiment: Bullish, Score: 0.650
```

#### 2. Announcement Summary

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

summary = summarizer.parse_announcement(
    text="Expected 2024 net profit growth of 20%, company decides on stock buyback",
    title="2024 Annual Earnings Forecast",
    publish_date="2025-01-15"
)

print(f"Type: {summary.announcement_type}")
print(f"Signal: {summary.investment_signal}")
# Output: Type: Earnings Forecast, Signal: Bullish
```

#### 3. Financial Report

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

report = reporter.create_report(
    stock_code="600519",
    company_name="Kweichow Moutai",
    financial_data={
        "revenue": 1500,
        "profit": 750,
        "eps": 60.0,
        "roe": 30.5,
        "pe": 35.0,
    }
)

# Terminal format output
print(reporter.format_terminal(report))

# JSON format output
print(reporter.format_json(report))

# Markdown format output
print(reporter.format_markdown(report))
```

#### 4. CLI Tool

```bash
# Sentiment analysis
finbuddy sentiment --text "Company earnings grew significantly"

# Batch sentiment analysis
finbuddy batch-sentiment --file news.txt

# Announcement summary
finbuddy announce --file announcement.txt --title "Earnings Forecast"

# Financial report
finbuddy financial --code 600519 --name "Kweichow Moutai" \
    --data '{"revenue":1500,"profit":750,"eps":60}'

# Comprehensive analysis
finbuddy analyze --code 600519 --name "Kweichow Moutai" \
    --news-file news.txt --fin-file financial.json
```

---

## 📖 Detailed Usage Guide

### Sentiment Analysis API

```python
from finbuddy import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# Single analysis
result = analyzer.analyze_text("Market sentiment is positive")

# Batch analysis
results = analyzer.analyze_batch([
    "Bullish news",
    "Bearish news",
    "Market stable"
])

# Market sentiment index
sentiment = analyzer.get_market_sentiment([
    {"title": "News 1", "content": "Earnings growth"},
    {"title": "News 2", "content": "Large orders"}
])
```

### Announcement Summary API

```python
from finbuddy import AnnouncementSummarizer

summarizer = AnnouncementSummarizer()

# Parse announcement
summary = summarizer.parse_announcement(
    text="Full announcement text...",
    title="Announcement title",
    publish_date="2025-01-15"
)

# Batch parsing
summaries = summarizer.parse_batch([
    {"text": "...", "title": "Earnings Forecast"},
    {"text": "...", "title": "Dividend Announcement"}
])

# Filter by signal
bullish = summarizer.filter_by_signal(summaries, "Bullish")
```

### Financial Report API

```python
from finbuddy import FinancialReporter

reporter = FinancialReporter()

# Create report
report = reporter.create_report(
    stock_code="600519",
    company_name="Kweichow Moutai",
    financial_data={
        "revenue": 1500,      # Operating revenue (100M CNY)
        "profit": 750,       # Net profit (100M CNY)
        "eps": 60.0,         # Earnings per share (CNY)
        "roe": 30.5,         # Return on equity (%)
        "pe": 35.0,          # P/E ratio
        "pb": 12.0,          # P/B ratio
    }
)

# Output formats
print(report.format_terminal())  # Terminal format
print(report.format_json())       # JSON format
print(report.format_markdown())   # Markdown format
```

### FinBuddyClient Integration Client

```python
from finbuddy import FinBuddyClient
from finbuddy.client import StockInfo

client = FinBuddyClient()

# Comprehensive analysis
result = client.comprehensive_analysis(
    stock=StockInfo(
        code="600519",
        name="Kweichow Moutai",
        market="SH",
        industry="Liquor",
        sector="Consumer"
    ),
    news=["Earnings growth", "New product launch"],
    announcements=[{"text": "...", "title": "Earnings Forecast"}],
    financial_data={"revenue": 1500, "profit": 750}
)

print(f"Overall Signal: {result.overall_signal}")
```

---

## 💡 Design Philosophy

### Technology Choices

- **Python 3.8+**: Wide compatibility, rich data science ecosystem
- **Rich**: Terminal beautification, improved readability
- **No LLM Dependency**: Core features based on dictionary, no API Key needed
- **Optional LLM**: Support OpenAI/Anthropic for deep analysis

### Architecture Design

```
finbuddy/
├── analyzer.py      # Sentiment analysis module
├── summarizer.py    # Announcement summary module
├── reporter.py      # Financial report module
├── client.py        # Integration client
└── cli.py           # CLI tool
```

### Future Roadmap

- [ ] Support more data sources (East Money, Tonghuashun, etc.)
- [ ] Add technical analysis module (K-line patterns, moving averages)
- [ ] Support more LLM backends (Claude, Gemini, Wenxin, etc.)
- [ ] Web interface and API service
- [ ] Support Hong Kong and US stocks

---

## 📦 Packaging and Deployment

### Build Package

```bash
# Build wheel package
python -m build

# Build source distribution
python -m build --sdist
```

### Dependency Installation

```bash
# Core dependencies only
pip install finbuddy

# With LLM support
pip install finbuddy[llm]

# Development dependencies
pip install finbuddy[dev]

# All dependencies
pip install finbuddy[all]
```

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  ⭐ If this project is helpful to you, please give us a Star!
</p>

<p align="center">
  © 2026 FinBuddy | MIT License
</p>
