"""
客户端集成测试
"""

import pytest
from finbuddy.client import FinBuddyClient, StockInfo


class TestFinBuddyClient:
    """FinBuddy客户端测试"""
    
    @pytest.fixture
    def client(self):
        return FinBuddyClient()
    
    def test_sentiment_analysis(self, client):
        """测试情绪分析"""
        result = client.analyze_sentiment("某公司业绩大幅增长")
        
        assert result.score > 0
        assert result.level.value != "未知"
    
    def test_batch_sentiment(self, client):
        """测试批量情绪分析"""
        texts = ["利好消息", "利空消息"]
        results = client.analyze_batch_sentiment(texts)
        
        assert len(results) == 2
        assert results[0].score > 0
        assert results[1].score < 0
    
    def test_summarize_announcement(self, client):
        """测试公告摘要"""
        text = """
        600519贵州茅台业绩预告
        
        预计2024年度实现营业收入约1500亿元，同比增长约18%。
        预计实现净利润约750亿元，同比增长约20%。
        """
        
        result = client.summarize_announcement(
            text, "2024年度业绩预告", "2025-01-15"
        )
        
        assert result.title == "2024年度业绩预告"
        assert result.announcement_type == "业绩预告"
        assert result.investment_signal in ["利好", "中性偏好"]
    
    def test_generate_financial_report(self, client):
        """测试财务报告生成"""
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 30.5,
            "pe": 35.0,
        }
        
        report = client.generate_financial_report(
            "600519", "贵州茅台", financial_data
        )
        
        assert report.stock_code == "600519"
        assert report.company_name == "贵州茅台"
    
    def test_comprehensive_analysis(self, client):
        """测试综合分析"""
        stock = StockInfo(
            code="600519",
            name="贵州茅台",
            market="SH",
            industry="白酒",
            sector="消费"
        )
        
        news = [
            "公司业绩大幅增长",
            "市场份额持续提升"
        ]
        
        announcements = [
            {
                "text": "预计净利润增长20%",
                "title": "业绩预告",
                "publish_date": "2025-01-15"
            }
        ]
        
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 30.5,
            "pe": 35.0,
        }
        
        result = client.comprehensive_analysis(
            stock, news, announcements, financial_data
        )
        
        assert result.stock.code == "600519"
        assert result.overall_signal in ["买入", "观望偏多", "中性"]
        assert result.confidence > 0
    
    def test_comprehensive_no_financial(self, client):
        """测试无财务数据的综合分析"""
        stock = StockInfo(
            code="000001",
            name="平安银行",
            market="SZ",
            industry="银行",
            sector="金融"
        )
        
        news = ["银行业绩稳健增长"]
        announcements = []
        
        result = client.comprehensive_analysis(
            stock, news, announcements
        )
        
        assert result.stock.code == "000001"
        assert result.financial_report is None
