"""
财务报告生成器单元测试
"""

import pytest
from finbuddy.reporter import FinancialReporter, ValuationLevel


class TestFinancialReporter:
    """财务报告生成器测试"""
    
    @pytest.fixture
    def reporter(self):
        return FinancialReporter()
    
    def test_create_report(self, reporter):
        """测试创建财务报告"""
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 30.5,
            "pe": 35.0,
            "pb": 12.0,
            "gross_margin": 90.0,
            "period": "2024年度"
        }
        
        report = reporter.create_report("600519", "贵州茅台", financial_data)
        
        assert report.stock_code == "600519"
        assert report.company_name == "贵州茅台"
        assert len(report.metrics) > 0
        assert report.valuation in ValuationLevel
        assert 0 <= report.valuation_score <= 100
    
    def test_low_valuation(self, reporter):
        """测试低估值识别"""
        financial_data = {
            "revenue": 500,
            "profit": 100,
            "eps": 8.0,
            "roe": 20.0,
            "pe": 10.0,
            "pb": 0.8,
        }
        
        report = reporter.create_report("000001", "某银行", financial_data)
        
        assert report.valuation in [ValuationLevel.VERY_LOW, ValuationLevel.LOW]
        assert report.valuation_score > 50
    
    def test_high_valuation(self, reporter):
        """测试高估值识别"""
        financial_data = {
            "revenue": 100,
            "profit": 10,
            "eps": 1.0,
            "roe": 5.0,
            "pe": 200.0,
            "pb": 50.0,
        }
        
        report = reporter.create_report("000002", "某科技", financial_data)
        
        assert report.valuation in [ValuationLevel.HIGH, ValuationLevel.VERY_HIGH]
        assert report.valuation_score < 50
    
    def test_format_terminal(self, reporter):
        """测试终端格式输出"""
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 30.5,
            "pe": 35.0,
        }
        
        report = reporter.create_report("600519", "贵州茅台", financial_data)
        output = reporter.format_terminal(report)
        
        assert "贵州茅台" in output
        assert "600519" in output
        assert "估值分析" in output
    
    def test_format_json(self, reporter):
        """测试JSON格式输出"""
        import json
        
        financial_data = {
            "revenue": 1200,
            "profit": 600,
        }
        
        report = reporter.create_report("600519", "贵州茅台", financial_data)
        output = reporter.format_json(report)
        
        data = json.loads(output)
        assert data["stock_code"] == "600519"
        assert data["company_name"] == "贵州茅台"
        assert "metrics" in data
    
    def test_format_markdown(self, reporter):
        """测试Markdown格式输出"""
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
        }
        
        report = reporter.create_report("600519", "贵州茅台", financial_data)
        output = reporter.format_markdown(report)
        
        assert "#" in output  # Markdown标题
        assert "贵州茅台" in output
        assert "估值分析" in output
    
    def test_risk_identification(self, reporter):
        """测试风险识别"""
        financial_data = {
            "revenue": 100,
            "profit": -20,
            "eps": -1.0,
            "roe": -5.0,
            "pe": -5.0,
            "debt_ratio": 85.0,
        }
        
        report = reporter.create_report("000001", "某公司", financial_data)
        
        assert len(report.risks) > 0
        assert any("资产负债率" in risk for risk in report.risks)
    
    def test_opportunity_identification(self, reporter):
        """测试机会识别"""
        financial_data = {
            "revenue": 1200,
            "profit": 600,
            "eps": 48.0,
            "roe": 35.0,
            "pe": 15.0,
            "revenue_yoy": 50.0,
        }
        
        report = reporter.create_report("600519", "贵州茅台", financial_data)
        
        assert len(report.opportunities) > 0
