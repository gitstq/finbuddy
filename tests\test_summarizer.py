"""
公告摘要生成器单元测试
"""

import pytest
from finbuddy.summarizer import AnnouncementSummarizer


class TestAnnouncementSummarizer:
    """公告摘要生成器测试"""
    
    @pytest.fixture
    def summarizer(self):
        return AnnouncementSummarizer()
    
    def test_performance_announcement(self, summarizer):
        """测试业绩预告公告"""
        text = """
        600519贵州茅台酒股份有限公司
        2024年度业绩预告公告
        
        经财务部门初步测算，预计2024年度实现营业收入约1500亿元，
        同比增长约18%。预计实现净利润约750亿元，同比增长约20%。
        每股收益约60元，同比增长20%。
        
        业绩增长主要原因：1）产品销量增加；2）产品结构优化；3）费用管控有效。
        """
        
        result = summarizer.parse_announcement(
            text, "2024年度业绩预告", "2025-01-15"
        )
        
        assert result.announcement_type == "业绩预告"
        assert result.investment_signal == "利好"
        assert len(result.key_points) > 0
        assert "600519" in result.stock_code
        assert "贵州" in result.company
    
    def test_dividend_announcement(self, summarizer):
        """测试分红公告"""
        text = """
        000002万科A分红派息公告
        
        公司决定向全体股东派发2024年度现金红利，每10股派发现金红利15元
        （含税），共计派发股息约170亿元。
        
        股权登记日：2025-04-20
        除权除息日：2025-04-21
        """
        
        result = summarizer.parse_announcement(
            text, "2024年度分红派息实施公告", "2025-04-10"
        )
        
        assert result.announcement_type == "分红派息"
        assert "15元" in str(result.key_points) or any("分红" in str(kp) for kp in result.key_points)
    
    def test_risk_warning_announcement(self, summarizer):
        """测试风险警示公告"""
        text = """
        *ST天龙风险警示公告
        
        因公司连续两年亏损，股票被实施退市风险警示。
        2024年度审计净利润为负值，营业收入低于1亿元。
        公司面临重大经营风险，提醒投资者注意投资风险。
        """
        
        result = summarizer.parse_announcement(
            text, "关于股票实施退市风险警示的公告", "2025-04-01"
        )
        
        assert result.announcement_type == "风险警示"
        assert result.investment_signal in ["利空", "中性偏空"]
    
    def test_empty_text(self, summarizer):
        """测试空文本"""
        result = summarizer.parse_announcement("", "空公告")
        
        assert result.title == "空公告"
        assert result.company == "未知"
        assert result.investment_signal == "中性"
    
    def test_parse_batch(self, summarizer):
        """测试批量解析"""
        announcements = [
            {
                "text": "某公司业绩大幅增长",
                "title": "业绩预告",
                "publish_date": "2025-01-01"
            },
            {
                "text": "某公司被处罚",
                "title": "监管函",
                "publish_date": "2025-01-02"
            }
        ]
        
        results = summarizer.parse_batch(announcements)
        
        assert len(results) == 2
        assert results[0].investment_signal in ["利好", "中性偏好"]
        assert results[1].investment_signal in ["利空", "中性偏空"]
    
    def test_filter_by_signal(self, summarizer):
        """测试按信号过滤"""
        results = [
            summarizer.parse_announcement("业绩增长100%", "业绩预告"),
            summarizer.parse_announcement("业绩下降50%", "业绩预警"),
            summarizer.parse_announcement("市场平稳", "日常公告")
        ]
        
        bullish = summarizer.filter_by_signal(results, "利好")
        bearish = summarizer.filter_by_signal(results, "利空")
        
        assert len(bullish) >= 1
        assert len(bearish) >= 1
    
    def test_extract_company_info(self, summarizer):
        """测试公司信息提取"""
        text_sh = "600519贵州茅台股份有限公司公告"
        text_sz = "000001平安银行股份有限公司公告"
        
        _, code_sh = summarizer._extract_company_info(text_sh)
        _, code_sz = summarizer._extract_company_info(text_sz)
        
        assert code_sh == "600519.SH"
        assert code_sz == "000001.SZ"
