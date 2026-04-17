"""
FinBuddy - A股金融情报助手
基于LLM的上市公司公告解读、市场情绪分析与财务数据智能分析工具
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .analyzer import SentimentAnalyzer
from .summarizer import AnnouncementSummarizer
from .reporter import FinancialReporter
from .client import FinBuddyClient

__all__ = [
    "SentimentAnalyzer",
    "AnnouncementSummarizer",
    "FinancialReporter",
    "FinBuddyClient",
]
