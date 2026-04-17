"""
FinBuddy 使用示例 - 客户端整合
"""

from finbuddy import FinBuddyClient
from finbuddy.client import StockInfo

# ============================================================
# 示例: FinBuddy 客户端
# ============================================================

# 初始化客户端（无需LLM也可使用基础功能）
client = FinBuddyClient()

# ============================================================
# 示例1: 快速情绪分析
# ============================================================
print("快速情绪分析:")
result = client.analyze_sentiment("某公司业绩大幅增长，利好消息")
print(f"  情绪: {result.level.value}, 分数: {result.score:.3f}")

# ============================================================
# 示例2: 公告摘要
# ============================================================
print("\n公告摘要:")
summary = client.summarize_announcement(
    text="预计净利润同比增长50%，公司决定进行股票回购",
    title="2024年度业绩预告",
    publish_date="2025-01-15"
)
print(f"  公司: {summary.company}")
print(f"  类型: {summary.announcement_type}")
print(f"  信号: {summary.investment_signal}")

# ============================================================
# 示例3: 财务报告
# ============================================================
print("\n财务报告:")
report = client.generate_financial_report(
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
print(f"  估值: {report.valuation.value} (评分: {report.valuation_score}/100)")
print(f"  摘要: {report.investment_summary}")

# ============================================================
# 示例4: 综合分析
# ============================================================
print("\n综合分析:")
stock = StockInfo(
    code="600519",
    name="贵州茅台",
    market="SH",
    industry="白酒",
    sector="消费"
)

news = [
    "公司业绩持续增长",
    "市场份额稳步提升",
    "新产品上市反响良好"
]

announcements = [
    {
        "text": "预计净利润增长20%",
        "title": "业绩预告",
        "publish_date": "2025-01-15"
    },
    {
        "text": "决定分红每股10元",
        "title": "分红公告",
        "publish_date": "2025-01-20"
    }
]

financial_data = {
    "revenue": 1500,
    "profit": 750,
    "eps": 60.0,
    "roe": 30.5,
    "pe": 35.0,
}

result = client.comprehensive_analysis(
    stock=stock,
    news=news,
    announcements=announcements,
    financial_data=financial_data
)

print(f"  股票: {result.stock.name} ({result.stock.code})")
print(f"  整体信号: {result.overall_signal}")
print(f"  置信度: {result.confidence:.1%}")

print("\n[完成]")
