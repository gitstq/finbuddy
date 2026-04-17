"""
FinBuddy 客户端
整合情绪分析、公告摘要、财务报表三大功能的核心API
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .analyzer import SentimentAnalyzer, SentimentResult
from .summarizer import AnnouncementSummarizer, AnnouncementSummary
from .reporter import FinancialReporter, FinancialReport


@dataclass
class StockInfo:
    """股票基本信息"""
    code: str
    name: str
    market: str  # SH/SZ
    industry: str
    sector: str


@dataclass
class AnalysisResult:
    """综合分析结果"""
    stock: StockInfo
    sentiment: Optional[SentimentResult]
    announcements: List[AnnouncementSummary]
    financial_report: Optional[FinancialReport]
    overall_signal: str  # 整体信号
    confidence: float


class FinBuddyClient:
    """
    FinBuddy 核心客户端
    
    使用示例:
        client = FinBuddyClient()
        
        # 分析市场情绪
        sentiment = client.analyze_sentiment("某公司业绩大幅增长...")
        
        # 解析公告
        summary = client.summarize_announcement(text)
        
        # 生成财务报告
        report = client.generate_financial_report("600519", "贵州茅台", {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 30.5,
            "pe": 35.0
        })
    """
    
    def __init__(self, llm_client=None):
        """
        初始化 FinBuddy 客户端
        
        Args:
            llm_client: 可选的LLM客户端（用于深度分析）
        """
        self.analyzer = SentimentAnalyzer(llm_client)
        self.summarizer = AnnouncementSummarizer(llm_client)
        self.reporter = FinancialReporter()
    
    def analyze_sentiment(self, text: str) -> SentimentResult:
        """
        分析文本情绪
        
        Args:
            text: 待分析文本
            
        Returns:
            SentimentResult: 情绪分析结果
        """
        return self.analyzer.analyze_text(text)
    
    def analyze_batch_sentiment(self, texts: List[str]) -> List[SentimentResult]:
        """
        批量分析情绪
        
        Args:
            texts: 文本列表
            
        Returns:
            List[SentimentResult]: 结果列表
        """
        return self.analyzer.analyze_batch(texts)
    
    def summarize_announcement(self, text: str, title: str = "",
                             publish_date: str = "") -> AnnouncementSummary:
        """
        摘要公告
        
        Args:
            text: 公告全文
            title: 公告标题
            publish_date: 发布日期
            
        Returns:
            AnnouncementSummary: 公告摘要
        """
        return self.summarizer.parse_announcement(text, title, publish_date)
    
    def summarize_batch_announcements(self, 
                                    announcements: List[Dict]) -> List[AnnouncementSummary]:
        """
        批量摘要公告
        
        Args:
            announcements: 公告列表
            
        Returns:
            List[AnnouncementSummary]: 摘要列表
        """
        return self.summarizer.parse_batch(announcements)
    
    def generate_financial_report(self, stock_code: str, company_name: str,
                                  financial_data: Dict) -> FinancialReport:
        """
        生成财务报告
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            financial_data: 财务数据
            
        Returns:
            FinancialReport: 财务报告
        """
        return self.reporter.create_report(stock_code, company_name, financial_data)
    
    def comprehensive_analysis(self, stock: StockInfo,
                              news: List[str],
                              announcements: List[Dict],
                              financial_data: Dict = None) -> AnalysisResult:
        """
        综合分析
        
        Args:
            stock: 股票信息
            news: 新闻列表
            announcements: 公告列表
            financial_data: 财务数据
            
        Returns:
            AnalysisResult: 综合分析结果
        """
        # 情绪分析
        sentiment = None
        if news:
            sentiment = self.analyzer.get_market_sentiment([
                {"title": "", "content": n} for n in news
            ])
            sentiment_result = SentimentResult(
                level=None,
                score=sentiment.get("score", 0),
                keywords=[],
                summary=f"基于{len(news)}条新闻分析",
                confidence=sentiment.get("confidence", 0)
            )
        
        # 公告摘要
        ann_summaries = []
        if announcements:
            ann_summaries = self.summarize_batch_announcements(announcements)
        
        # 财务报告
        fin_report = None
        if financial_data:
            fin_report = self.generate_financial_report(
                stock.code, stock.name, financial_data
            )
        
        # 整体信号
        overall_signal = self._calculate_overall_signal(
            sentiment, ann_summaries, fin_report
        )
        
        return AnalysisResult(
            stock=stock,
            sentiment=sentiment_result if news else None,
            announcements=ann_summaries,
            financial_report=fin_report,
            overall_signal=overall_signal,
            confidence=0.7
        )
    
    def _calculate_overall_signal(self, sentiment, announcements: List, 
                                  report) -> str:
        """计算整体信号"""
        bullish = 0
        bearish = 0
        
        # 情绪分数
        if sentiment and sentiment.score > 0.2:
            bullish += 1
        elif sentiment and sentiment.score < -0.2:
            bearish += 1
        
        # 公告信号
        for ann in announcements:
            if ann.investment_signal in ["利好", "中性偏好"]:
                bullish += 1
            elif ann.investment_signal in ["利空", "中性偏空"]:
                bearish += 1
        
        # 财务信号
        if report:
            if report.valuation_score > 60:
                bullish += 1
            elif report.valuation_score < 40:
                bearish += 1
        
        if bullish > bearish + 1:
            return "买入"
        elif bearish > bullish + 1:
            return "卖出"
        elif bullish > 0:
            return "观望偏多"
        elif bearish > 0:
            return "观望偏空"
        return "中性"
