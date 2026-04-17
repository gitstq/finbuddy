"""
情绪分析器单元测试
"""

import pytest
from finbuddy.analyzer import SentimentAnalyzer, SentimentLevel


class TestSentimentAnalyzer:
    """情绪分析器测试"""
    
    @pytest.fixture
    def analyzer(self):
        return SentimentAnalyzer()
    
    def test_positive_sentiment(self, analyzer):
        """测试正面情绪识别"""
        text = "某公司业绩大幅增长，净利润同比增长50%，订单量创新高，市场份额持续扩张"
        result = analyzer.analyze_text(text)
        
        assert result.score > 0.2
        assert result.level in [SentimentLevel.BULLISH, SentimentLevel.VERY_BULLISH]
    
    def test_negative_sentiment(self, analyzer):
        """测试负面情绪识别"""
        text = "公司业绩大幅下降，净利润同比减少60%，面临债务违约风险，被监管部门处罚"
        result = analyzer.analyze_text(text)
        
        assert result.score < -0.2
        assert result.level in [SentimentLevel.BEARISH, SentimentLevel.VERY_BEARISH]
    
    def test_neutral_sentiment(self, analyzer):
        """测试中性情绪"""
        text = "今日市场交易活跃，成交量与昨日基本持平"
        result = analyzer.analyze_text(text)
        
        assert abs(result.score) <= 0.2
        assert result.level == SentimentLevel.NEUTRAL
    
    def test_empty_text(self, analyzer):
        """测试空文本"""
        result = analyzer.analyze_text("")
        
        assert result.score == 0.0
        assert result.confidence == 0.0
        assert result.summary == "文本为空"
    
    def test_keywords_extraction(self, analyzer):
        """测试关键词提取"""
        text = "业绩增长100%，回购股票5000万股"
        result = analyzer.analyze_text(text)
        
        assert len(result.keywords) > 0
        assert any("+" in kw for kw in result.keywords)
    
    def test_batch_analysis(self, analyzer):
        """测试批量分析"""
        texts = [
            "业绩大幅增长，利好",
            "风险提示，利空",
            "市场平稳，中性"
        ]
        
        results = analyzer.analyze_batch(texts)
        
        assert len(results) == 3
        assert results[0].score > 0
        assert results[1].score < 0
    
    def test_market_sentiment(self, analyzer):
        """测试市场情绪"""
        news_list = [
            {"title": "某公司业绩增长", "content": "净利润同比增长50%"},
            {"title": "行业龙头扩张", "content": "市场份额持续提升"},
            {"title": "政策利好", "content": "行业获得政策支持"}
        ]
        
        result = analyzer.get_market_sentiment(news_list)
        
        assert "sentiment" in result
        assert result["sentiment"] in ["bullish", "bearish", "neutral"]
        assert result["news_count"] == 3
        assert result["score"] > 0  # 正面新闻为主
    
    def test_empty_news_list(self, analyzer):
        """测试空新闻列表"""
        result = analyzer.get_market_sentiment([])
        
        assert result["sentiment"] == "neutral"
        assert result["news_count"] == 0
