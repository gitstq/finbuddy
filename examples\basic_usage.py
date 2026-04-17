"""
FinBuddy 使用示例 - 基础功能
"""

from finbuddy import (
    SentimentAnalyzer,
    AnnouncementSummarizer,
    FinancialReporter
)

# ============================================================
# 示例1: 情绪分析
# ============================================================
print("=" * 60)
print("示例1: 情绪分析")
print("=" * 60)

analyzer = SentimentAnalyzer()

# 分析单条文本
text = """
贵州茅台发布业绩预告，预计2024年度实现营业收入约1500亿元，
同比增长约18%。预计实现净利润约750亿元，同比增长约20%。
公司产品销量持续增长，市场份额稳步提升。
"""

result = analyzer.analyze_text(text)
print(f"情绪等级: {result.level.value}")
print(f"情绪分数: {result.score:.3f}")
print(f"确信度: {result.confidence:.1%}")
print(f"关键词: {result.keywords}")
print(f"摘要: {result.summary}")

# ============================================================
# 示例2: 批量情绪分析
# ============================================================
print("\n" + "=" * 60)
print("示例2: 批量情绪分析")
print("=" * 60)

news_list = [
    {"title": "某公司业绩大增", "content": "净利润同比增长50%，超预期"},
    {"title": "行业政策利好", "content": "政策支持行业发展，企业迎来新机遇"},
    {"title": "市场竞争加剧", "content": "多家企业进入，市场竞争日趋激烈"}
]

sentiment = analyzer.get_market_sentiment(news_list)
print(f"整体情绪: {sentiment['sentiment']}")
print(f"情绪分数: {sentiment['score']:.3f}")
print(f"新闻数量: {sentiment['news_count']}")
print(f"看多数量: {sentiment['bullish_count']}")
print(f"看空数量: {sentiment['bearish_count']}")
print(f"中性数量: {sentiment['neutral_count']}")

# ============================================================
# 示例3: 公告摘要
# ============================================================
print("\n" + "=" * 60)
print("示例3: 公告摘要")
print("=" * 60)

summarizer = AnnouncementSummarizer()

announcement = """
600519贵州茅台酒股份有限公司
2024年度业绩预告公告

经财务部门初步测算，预计2024年度实现营业收入约1500亿元，
同比增长约18%。预计实现净利润约750亿元，同比增长约20%。
每股收益约60元，同比增长20%。

业绩增长主要原因：
1）产品销量增加
2）产品结构优化
3）费用管控有效

请广大投资者注意投资风险。
"""

summary = summarizer.parse_announcement(
    announcement,
    "2024年度业绩预告公告",
    "2025-01-15"
)

print(f"公司: {summary.company} ({summary.stock_code})")
print(f"公告类型: {summary.announcement_type}")
print(f"投资信号: {summary.investment_signal}")
print(f"\n关键点:")
for i, point in enumerate(summary.key_points, 1):
    print(f"  {i}. {point}")

if summary.risk_factors:
    print(f"\n风险提示:")
    for risk in summary.risk_factors:
        print(f"  ⚠️ {risk}")

print(f"\n摘要: {summary.summary}")

# ============================================================
# 示例4: 财务报告
# ============================================================
print("\n" + "=" * 60)
print("示例4: 财务报告")
print("=" * 60)

reporter = FinancialReporter()

financial_data = {
    "revenue": 1500,          # 营业收入（亿元）
    "profit": 750,            # 净利润（亿元）
    "eps": 60.0,              # 每股收益（元）
    "roe": 30.5,              # 净资产收益率（%）
    "pe": 35.0,               # 市盈率
    "pb": 12.0,               # 市净率
    "gross_margin": 90.0,     # 毛利率（%）
    "net_margin": 50.0,       # 净利率（%）
    "debt_ratio": 25.0,       # 资产负债率（%）
    "period": "2024年度"
}

report = reporter.create_report("600519", "贵州茅台", financial_data)

# 终端格式输出
print(reporter.format_terminal(report))

print("\n[完成]")
