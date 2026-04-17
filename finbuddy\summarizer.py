"""
公告摘要生成器
利用LLM自动生成A股上市公司公告的关键信息摘要
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import re


@dataclass
class AnnouncementSummary:
    """公告摘要"""
    title: str
    company: str
    stock_code: str
    announcement_type: str  # 公告类型
    publish_date: str
    key_points: List[str]  # 关键点
    risk_factors: List[str]  # 风险提示
    investment_signal: str  # 投资信号: 利好/利空/中性
    summary: str  # 完整摘要
    raw_text: str  # 原始文本（保留）


class AnnouncementSummarizer:
    """
    A股公告摘要生成器
    
    功能：
    - 自动识别公告类型
    - 提取关键信息和数据
    - 生成结构化摘要
    - 判断投资信号
    """
    
    # 公告类型关键词映射
    TYPE_KEYWORDS = {
        "业绩预告": ["业绩预告", "业绩预增", "业绩预减", "业绩快报"],
        "分红派息": ["分红", "派息", "送股", "转增"],
        "股权变动": ["增持", "减持", "回购", "发行", "募资"],
        "重大合同": ["合同", "订单", "中标", "合作协议"],
        "风险警示": ["风险警示", "ST", "退市风险", "诉讼"],
        "资产重组": ["重组", "并购", "收购", "资产出售"],
        "人事变动": ["人事", "高管", "董事", "监事", "辞职", "任命"],
        "监管问询": ["问询函", "监管函", "核查", "审查"],
    }
    
    # 投资信号关键词
    BULLISH_SIGNALS = [
        "业绩预增", "大幅增长", "超预期", "回购", "增持", "中标",
        "战略合作", "新产品", "新市场", "产能扩张", "分红增加"
    ]
    
    BEARISH_SIGNALS = [
        "业绩预减", "大幅下降", "不及预期", "减持", "诉讼",
        "风险警示", "ST", "退市风险", "商誉减值", "债务风险"
    ]
    
    def __init__(self, llm_client=None):
        """
        初始化公告摘要生成器
        
        Args:
            llm_client: LLM客户端
        """
        self.llm_client = llm_client
    
    def parse_announcement(self, text: str, title: str = "", 
                          publish_date: str = "") -> AnnouncementSummary:
        """
        解析并摘要公告
        
        Args:
            text: 公告全文
            title: 公告标题
            publish_date: 发布日期
            
        Returns:
            AnnouncementSummary: 结构化摘要
        """
        if not text:
            return self._empty_summary(title, publish_date)
        
        # 提取公司信息和股票代码
        company, stock_code = self._extract_company_info(text)
        
        # 判断公告类型
        ann_type = self._classify_announcement(title, text)
        
        # 提取关键点
        key_points = self._extract_key_points(title, text, ann_type)
        
        # 提取风险因素
        risk_factors = self._extract_risk_factors(text)
        
        # 判断投资信号
        investment_signal = self._judge_signal(title, text, key_points)
        
        # 生成摘要
        summary = self._generate_summary(title, company, ann_type, 
                                         key_points, investment_signal)
        
        return AnnouncementSummary(
            title=title or "未知标题",
            company=company or "未知公司",
            stock_code=stock_code or "未知代码",
            announcement_type=ann_type,
            publish_date=publish_date or datetime.now().strftime("%Y-%m-%d"),
            key_points=key_points,
            risk_factors=risk_factors,
            investment_signal=investment_signal,
            summary=summary,
            raw_text=text[:5000]  # 保留前5000字符
        )
    
    def parse_batch(self, announcements: List[Dict]) -> List[AnnouncementSummary]:
        """
        批量解析公告
        
        Args:
            announcements: 公告列表，每项包含 text, title, publish_date
            
        Returns:
            List[AnnouncementSummary]: 摘要列表
        """
        results = []
        for ann in announcements:
            summary = self.parse_announcement(
                text=ann.get("text", ""),
                title=ann.get("title", ""),
                publish_date=ann.get("publish_date", "")
            )
            results.append(summary)
        return results
    
    def filter_by_signal(self, summaries: List[AnnouncementSummary], 
                        signal: str) -> List[AnnouncementSummary]:
        """
        按投资信号过滤公告
        
        Args:
            summaries: 摘要列表
            signal: 信号类型 (利好/利空/中性)
            
        Returns:
            List[AnnouncementSummary]: 过滤后的列表
        """
        return [s for s in summaries if s.investment_signal == signal]
    
    def _extract_company_info(self, text: str) -> tuple:
        """提取公司名称和股票代码"""
        # 股票代码模式
        code_pattern = r"(\d{6})"
        code_match = re.search(code_pattern, text[:500])
        
        # 公司名称模式（简化）
        company_pattern = r"([\u4e00-\u9fa5]{2,20}(?:股份|集团|公司|有限))"
        company_match = re.search(company_pattern, text[:500])
        
        stock_code = code_match.group(1) if code_match else ""
        # 添加交易所后缀
        if stock_code:
            if stock_code.startswith(("6", "5")):
                stock_code += ".SH"
            else:
                stock_code += ".SZ"
        
        company = company_match.group(1) if company_match else ""
        return company, stock_code
    
    def _classify_announcement(self, title: str, text: str) -> str:
        """分类公告类型"""
        combined = f"{title} {text[:1000]}"
        
        for ann_type, keywords in self.TYPE_KEYWORDS.items():
            for kw in keywords:
                if kw in combined:
                    return ann_type
        return "其他公告"
    
    def _extract_key_points(self, title: str, text: str, ann_type: str) -> List[str]:
        """提取关键点"""
        key_points = []
        
        # 基于类型提取对应关键点
        if ann_type == "业绩预告":
            # 提取业绩数据
            numbers = re.findall(r"[\d.]+[%亿元万元]", text[:2000])
            if numbers:
                key_points.append(f"业绩相关数据：{', '.join(numbers[:5])}")
        
        elif ann_type == "分红派息":
            # 提取分红方案
            div_pattern = r"(?:每股|每10股)[^\n]{0,50}"
            div_match = re.findall(div_pattern, text[:1000])
            if div_match:
                key_points.extend([f"分红方案：{d.strip()}" for d in div_match[:3]])
        
        elif ann_type == "股权变动":
            # 提取变动比例
            pct_pattern = r"\d+[%‰]?[增持减持]"
            pct_match = re.findall(pct_pattern, text[:1000])
            if pct_match:
                key_points.extend(pct_match[:3])
        
        elif ann_type == "重大合同":
            # 提取合同金额
            amount_pattern = r"[\d.]+[亿万]元"
            amount_match = re.findall(amount_pattern, text[:1000])
            if amount_match:
                key_points.append(f"合同金额：{', '.join(set(amount_match[:3]))}")
        
        # 提取数字信息
        numbers = re.findall(r"(?:营收|收入|利润|增长|下降|同比)[^\d]{0,10}[\d.]+[%亿万元]?", text[:2000])
        if numbers:
            key_points.extend([n.strip() for n in numbers[:5] if len(n.strip()) > 5])
        
        # 提取关键句子
        sentences = re.split(r"[。！？\n]", text[:1500])
        important_sentences = [s.strip() for s in sentences if any(
            kw in s for kw in ["重要", "关键", "主要", "核心", "公告"]
        ) and len(s.strip()) > 10]
        
        if important_sentences and len(key_points) < 3:
            key_points.extend(important_sentences[:3])
        
        return key_points[:10]  # 最多10个关键点
    
    def _extract_risk_factors(self, text: str) -> List[str]:
        """提取风险因素"""
        risk_keywords = [
            "风险", "不确定", "可能", "无法", "不能", "损失",
            "诉讼", "处罚", "调查", "违规", "减持风险"
        ]
        
        risk_factors = []
        sentences = text.split("。")
        
        for sent in sentences:
            if any(kw in sent for kw in risk_keywords) and len(sent.strip()) > 10:
                risk_factors.append(sent.strip()[:100])
        
        return risk_factors[:5]
    
    def _judge_signal(self, title: str, text: str, key_points: List[str]) -> str:
        """判断投资信号"""
        combined = f"{title} {' '.join(key_points)} {text[:500]}"
        
        bullish_count = sum(1 for s in self.BULLISH_SIGNALS if s in combined)
        bearish_count = sum(1 for s in self.BEARISH_SIGNALS if s in combined)
        
        if bullish_count > bearish_count + 1:
            return "利好"
        elif bearish_count > bullish_count + 1:
            return "利空"
        elif bullish_count > 0:
            return "中性偏好"
        elif bearish_count > 0:
            return "中性偏空"
        return "中性"
    
    def _generate_summary(self, title: str, company: str, ann_type: str,
                         key_points: List[str], signal: str) -> str:
        """生成完整摘要"""
        parts = []
        
        if company:
            parts.append(f"{company}发布")
        else:
            parts.append("某公司发布")
        
        parts.append(ann_type)
        
        if key_points:
            parts.append("，主要内容包括：")
            parts.append("；".join(key_points[:3]))
        else:
            parts.append("。")
        
        parts.append(f"整体呈{signal}信号。")
        
        return "".join(parts)
    
    def _empty_summary(self, title: str, publish_date: str) -> AnnouncementSummary:
        """返回空摘要"""
        return AnnouncementSummary(
            title=title or "未知",
            company="未知",
            stock_code="",
            announcement_type="其他",
            publish_date=publish_date,
            key_points=[],
            risk_factors=[],
            investment_signal="中性",
            summary="文本为空，无法生成摘要",
            raw_text=""
        )
