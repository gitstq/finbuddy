"""
财务数据报表生成器
生成股票财务分析报告、估值对比与投资建议摘要
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class ValuationLevel(Enum):
    """估值等级"""
    VERY_LOW = "极低"
    LOW = "偏低"
    FAIR = "合理"
    HIGH = "偏高"
    VERY_HIGH = "极高"


@dataclass
class FinancialMetric:
    """财务指标"""
    name: str
    value: float
    unit: str
    period: str
    yoy_change: Optional[float] = None  # 同比变化


@dataclass
class FinancialReport:
    """财务分析报告"""
    stock_code: str
    company_name: str
    report_date: str
    metrics: List[FinancialMetric]
    valuation: ValuationLevel
    valuation_score: float  # 0-100
    investment_summary: str
    risks: List[str]
    opportunities: List[str]


class FinancialReporter:
    """
    财务数据分析与报告生成器
    
    功能：
    - 计算关键财务指标
    - 估值分析与对比
    - 生成结构化分析报告
    - 输出多格式报告（Terminal/JSON/Markdown）
    """
    
    def __init__(self):
        """初始化财务报告生成器"""
        self.report_cache = {}
    
    def create_report(self, stock_code: str, company_name: str,
                     financial_data: Dict) -> FinancialReport:
        """
        创建财务分析报告
        
        Args:
            stock_code: 股票代码
            company_name: 公司名称
            financial_data: 财务数据字典
            
        Returns:
            FinancialReport: 分析报告
        """
        # 解析财务指标
        metrics = self._parse_metrics(financial_data)
        
        # 估值分析
        valuation, valuation_score = self._analyze_valuation(metrics)
        
        # 风险与机会
        risks = self._identify_risks(metrics, financial_data)
        opportunities = self._identify_opportunities(metrics, financial_data)
        
        # 生成摘要
        summary = self._generate_summary(stock_code, company_name, 
                                        metrics, valuation, valuation_score)
        
        return FinancialReport(
            stock_code=stock_code,
            company_name=company_name,
            report_date=datetime.now().strftime("%Y-%m-%d"),
            metrics=metrics,
            valuation=valuation,
            valuation_score=valuation_score,
            investment_summary=summary,
            risks=risks,
            opportunities=opportunities
        )
    
    def format_terminal(self, report: FinancialReport) -> str:
        """
        格式化为终端输出样式
        
        Args:
            report: 财务报告
            
        Returns:
            str: 格式化文本
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"  {report.company_name} ({report.stock_code}) 财务分析报告")
        lines.append(f"  报告日期: {report.report_date}")
        lines.append("=" * 60)
        
        # 估值
        lines.append(f"\n📊 估值分析: {report.valuation.value} (评分: {report.valuation_score}/100)")
        
        # 关键指标
        if report.metrics:
            lines.append("\n📈 关键财务指标:")
            for m in report.metrics[:8]:
                yoy_str = f" | 同比: {m.yoy_change:+.1f}%" if m.yoy_change else ""
                lines.append(f"  • {m.name}: {m.value:.2f} {m.unit}{yoy_str}")
        
        # 机会
        if report.opportunities:
            lines.append("\n✨ 投资机会:")
            for opp in report.opportunities:
                lines.append(f"  🔹 {opp}")
        
        # 风险
        if report.risks:
            lines.append("\n⚠️ 风险提示:")
            for risk in report.risks:
                lines.append(f"  🔸 {risk}")
        
        # 摘要
        lines.append(f"\n💡 投资摘要:\n  {report.investment_summary}")
        
        lines.append("\n" + "=" * 60)
        lines.append("⚠️ 免责声明: 本报告仅供参考，不构成投资建议")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def format_json(self, report: FinancialReport) -> str:
        """
        格式化为JSON
        
        Args:
            report: 财务报告
            
        Returns:
            str: JSON字符串
        """
        data = {
            "stock_code": report.stock_code,
            "company_name": report.company_name,
            "report_date": report.report_date,
            "valuation": {
                "level": report.valuation.value,
                "score": report.valuation_score
            },
            "metrics": [
                {
                    "name": m.name,
                    "value": m.value,
                    "unit": m.unit,
                    "period": m.period,
                    "yoy_change": m.yoy_change
                }
                for m in report.metrics
            ],
            "risks": report.risks,
            "opportunities": report.opportunities,
            "investment_summary": report.investment_summary,
            "disclaimer": "本报告仅供参考，不构成投资建议"
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def format_markdown(self, report: FinancialReport) -> str:
        """
        格式化为Markdown
        
        Args:
            report: 财务报告
            
        Returns:
            str: Markdown文本
        """
        md = []
        md.append(f"# {report.company_name} ({report.stock_code}) 财务分析报告")
        md.append(f"\n**报告日期**: {report.report_date}")
        md.append("\n## 估值分析")
        md.append(f"\n| 指标 | 数值 |")
        md.append("|------|------|")
        md.append(f"| 估值等级 | {report.valuation.value} |")
        md.append(f"| 估值评分 | {report.valuation_score}/100 |")
        
        if report.metrics:
            md.append("\n## 关键财务指标")
            md.append("\n| 指标名称 | 数值 | 单位 | 期间 | 同比变化 |")
            md.append("|----------|------|------|------|----------|")
            for m in report.metrics:
                yoy = f"{m.yoy_change:+.1f}%" if m.yoy_change else "-"
                md.append(f"| {m.name} | {m.value:.2f} | {m.unit} | {m.period} | {yoy} |")
        
        if report.opportunities:
            md.append("\n## 投资机会")
            for opp in report.opportunities:
                md.append(f"- {opp}")
        
        if report.risks:
            md.append("\n## 风险提示")
            for risk in report.risks:
                md.append(f"- {risk}")
        
        md.append("\n## 投资摘要")
        md.append(f"\n{report.investment_summary}")
        
        md.append("\n---\n")
        md.append("*⚠️ 免责声明: 本报告仅供参考，不构成投资建议*")
        
        return "\n".join(md)
    
    def _parse_metrics(self, data: Dict) -> List[FinancialMetric]:
        """解析财务指标"""
        metrics = []
        
        # 基础财务指标映射
        metric_map = {
            "revenue": ("营业收入", "亿元"),
            "profit": ("净利润", "亿元"),
            "eps": ("每股收益", "元"),
            "roe": ("净资产收益率", "%"),
            "pe": ("市盈率", "倍"),
            "pb": ("市净率", "倍"),
            "gross_margin": ("毛利率", "%"),
            "net_margin": ("净利率", "%"),
            "debt_ratio": ("资产负债率", "%"),
            "current_ratio": ("流动比率", "倍"),
        }
        
        for key, (name, unit) in metric_map.items():
            if key in data:
                metrics.append(FinancialMetric(
                    name=name,
                    value=float(data[key]),
                    unit=unit,
                    period=data.get("period", "最近季度"),
                    yoy_change=data.get(f"{key}_yoy")
                ))
        
        return metrics
    
    def _analyze_valuation(self, metrics: List[FinancialMetric]) -> tuple:
        """分析估值"""
        # 提取PE和PB
        pe = None
        pb = None
        for m in metrics:
            if m.name == "市盈率":
                pe = m.value
            elif m.name == "市净率":
                pb = m.value
        
        # 简化估值逻辑
        if pe and pb:
            # 简单估值判断
            score = 50  # 基础分
            
            if pe < 15:
                score += 25
                level = ValuationLevel.VERY_LOW
            elif pe < 25:
                score += 10
                level = ValuationLevel.LOW
            elif pe < 40:
                level = ValuationLevel.FAIR
            elif pe < 60:
                score -= 10
                level = ValuationLevel.HIGH
            else:
                score -= 25
                level = ValuationLevel.VERY_HIGH
            
            if pb and pb < 1:
                score += 10
            elif pb and pb > 5:
                score -= 10
            
            score = max(0, min(100, score))
            return level, score
        
        return ValuationLevel.FAIR, 50
    
    def _identify_risks(self, metrics: List[FinancialMetric], 
                       data: Dict) -> List[str]:
        """识别风险"""
        risks = []
        
        for m in metrics:
            if m.name == "资产负债率" and m.value > 70:
                risks.append(f"资产负债率偏高({m.value:.1f}%)，偿债压力较大")
            if m.name == "净资产收益率" and m.value < 5:
                risks.append(f"净资产收益率较低({m.value:.1f}%)，盈利能力不足")
            if m.yoy_change and m.yoy_change < -30:
                risks.append(f"{m.name}同比大幅下降({m.yoy_change:.1f}%)")
        
        if not risks:
            risks.append("未发现明显财务风险")
        
        return risks[:3]
    
    def _identify_opportunities(self, metrics: List[FinancialMetric],
                               data: Dict) -> List[str]:
        """识别机会"""
        opportunities = []
        
        for m in metrics:
            if m.name == "净资产收益率" and m.value > 15:
                opportunities.append(f"净资产收益率优秀({m.value:.1f}%)，股东回报率高")
            if m.yoy_change and m.yoy_change > 30:
                opportunities.append(f"{m.name}同比大幅增长({m.yoy_change:.1f}%)，成长性强")
            if m.name == "市盈率" and m.value < 20:
                opportunities.append(f"市盈率较低({m.value:.1f}倍)，估值有优势")
        
        if not opportunities:
            opportunities.append("财务指标处于正常区间")
        
        return opportunities[:3]
    
    def _generate_summary(self, stock_code: str, company_name: str,
                         metrics: List[FinancialMetric], 
                         valuation: ValuationLevel,
                         valuation_score: float) -> str:
        """生成投资摘要"""
        parts = []
        
        parts.append(f"{company_name}({stock_code})")
        
        if valuation == ValuationLevel.VERY_LOW or valuation == ValuationLevel.LOW:
            parts.append("当前估值偏低，具有一定估值修复空间")
        elif valuation == ValuationLevel.HIGH or valuation == ValuationLevel.VERY_HIGH:
            parts.append("当前估值偏高，需注意回调风险")
        else:
            parts.append("当前估值处于合理区间")
        
        return "".join(parts) + "。建议结合基本面综合判断。"
