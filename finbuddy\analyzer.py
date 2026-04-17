"""
市场情绪分析器
利用LLM分析A股市场情绪、行业热点与舆情倾向
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json


class SentimentLevel(Enum):
    """情绪等级"""
    VERY_BEARISH = "极度悲观"
    BEARISH = "偏悲观"
    NEUTRAL = "中性"
    BULLISH = "偏乐观"
    VERY_BULLISH = "极度乐观"


@dataclass
class SentimentResult:
    """情绪分析结果"""
    level: SentimentLevel
    score: float  # -1.0 到 1.0
    keywords: List[str]
    summary: str
    confidence: float  # 0.0 到 1.0


class SentimentAnalyzer:
    """
    A股市场情绪分析器
    
    功能：
    - 分析新闻/公告情绪倾向
    - 判断市场整体情绪状态
    - 提取关键情绪因子
    """
    
    # 中文金融情绪词典
    POSITIVE_KEYWORDS = [
        "增长", "盈利", "突破", "创新", "扩张", "合作", "订单",
        "超预期", "龙头", "领涨", "涨停", "增持", "买入", "推荐",
        "上调", "超卖", "复苏", "景气", "向好", "利润", "分红",
        "回购", "重组", "并购", "景气上行", "市场份额提升"
    ]
    
    NEGATIVE_KEYWORDS = [
        "下降", "亏损", "风险", "警示", "减持", "卖出", "下调",
        "不及预期", "暴雷", "造假", "处罚", "诉讼", "债务",
        "违约", "裁员", "破产", "退市", "ST", "戴帽", "商誉",
        "存货", "应收款", "资金链", "监管", "调查", "召回"
    ]
    
    def __init__(self, llm_client=None):
        """
        初始化情绪分析器
        
        Args:
            llm_client: LLM客户端（支持OpenAI/Anthropic格式）
        """
        self.llm_client = llm_client
    
    def analyze_text(self, text: str) -> SentimentResult:
        """
        分析单条文本的情绪倾向
        
        Args:
            text: 待分析的文本内容
            
        Returns:
            SentimentResult: 情绪分析结果
        """
        if not text or not text.strip():
            return SentimentResult(
                level=SentimentLevel.NEUTRAL,
                score=0.0,
                keywords=[],
                summary="文本为空",
                confidence=0.0
            )
        
        # 基础关键词分析
        pos_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text)
        neg_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text)
        total = pos_count + neg_count
        
        if total == 0:
            base_score = 0.0
            confidence = 0.3
        else:
            base_score = (pos_count - neg_count) / total
            confidence = min(0.5 + (total * 0.1), 0.95)
        
        # LLM深度分析（如果可用）
        if self.llm_client:
            try:
                llm_result = self._llm_analyze(text)
                if llm_result:
                    return llm_result
            except Exception:
                pass
        
        # 返回基于词典的结果
        return self._build_result(text, base_score, confidence, pos_count, neg_count)
    
    def analyze_batch(self, texts: List[str]) -> List[SentimentResult]:
        """
        批量分析文本情绪
        
        Args:
            texts: 文本列表
            
        Returns:
            List[SentimentResult]: 分析结果列表
        """
        return [self.analyze_text(text) for text in texts]
    
    def get_market_sentiment(self, news_list: List[Dict]) -> Dict:
        """
        计算市场整体情绪指数
        
        Args:
            news_list: 新闻/公告列表，每项包含 'title' 和 'content'
            
        Returns:
            Dict: 市场情绪报告
        """
        if not news_list:
            return {"sentiment": "neutral", "score": 0.0, "news_count": 0}
        
        results = []
        for item in news_list:
            text = f"{item.get('title', '')} {item.get('content', '')}"
            results.append(self.analyze_text(text))
        
        avg_score = sum(r.score for r in results) / len(results)
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        bullish = sum(1 for r in results if r.score > 0.2)
        bearish = sum(1 for r in results if r.score < -0.2)
        
        return {
            "sentiment": self._score_to_sentiment(avg_score),
            "score": round(avg_score, 3),
            "confidence": round(avg_confidence, 3),
            "news_count": len(news_list),
            "bullish_count": bullish,
            "bearish_count": bearish,
            "neutral_count": len(news_list) - bullish - bearish
        }
    
    def _llm_analyze(self, text: str) -> Optional[SentimentResult]:
        """调用LLM进行深度情绪分析"""
        if not self.llm_client:
            return None
        
        prompt = f"""分析以下A股相关文本的情绪倾向，判断是利好还是利空。

文本内容：
{text[:2000]}

请以JSON格式返回分析结果：
{{
    "sentiment": "bullish/bearish/neutral",
    "score": -1.0到1.0的情绪分数,
    "summary": "一句话总结情绪倾向",
    "confidence": 0.0到1.0的确信度
}}"""

        response = self.llm_client.generate(prompt)
        try:
            data = json.loads(response)
            level = {
                "very_bullish": SentimentLevel.VERY_BULLISH,
                "bullish": SentimentLevel.BULLISH,
                "neutral": SentimentLevel.NEUTRAL,
                "bearish": SentimentLevel.BEARISH,
                "very_bearish": SentimentLevel.VERY_BEARISH
            }.get(data.get("sentiment", "neutral"), SentimentLevel.NEUTRAL)
            
            return SentimentResult(
                level=level,
                score=float(data.get("score", 0)),
                keywords=[],
                summary=data.get("summary", ""),
                confidence=float(data.get("confidence", 0.5))
            )
        except (json.JSONDecodeError, KeyError):
            return None
    
    def _build_result(self, text: str, score: float, confidence: float, 
                      pos_count: int, neg_count: int) -> SentimentResult:
        """构建基于词典的分析结果"""
        keywords = []
        for kw in self.POSITIVE_KEYWORDS:
            if kw in text:
                keywords.append(f"+{kw}")
        for kw in self.NEGATIVE_KEYWORDS:
            if kw in text:
                keywords.append(f"-{kw}")
        
        level = self._score_to_level(score)
        summary = self._generate_summary(score, pos_count, neg_count)
        
        return SentimentResult(
            level=level,
            score=round(score, 3),
            keywords=keywords[:10],  # 最多10个关键词
            summary=summary,
            confidence=round(confidence, 3)
        )
    
    def _score_to_level(self, score: float) -> SentimentLevel:
        """分数转换为情绪等级"""
        if score >= 0.6:
            return SentimentLevel.VERY_BULLISH
        elif score >= 0.2:
            return SentimentLevel.BULLISH
        elif score <= -0.6:
            return SentimentLevel.VERY_BEARISH
        elif score <= -0.2:
            return SentimentLevel.BEARISH
        return SentimentLevel.NEUTRAL
    
    def _score_to_sentiment(self, score: float) -> str:
        """分数转换为情绪标签"""
        if score > 0.3:
            return "bullish"
        elif score < -0.3:
            return "bearish"
        return "neutral"
    
    def _generate_summary(self, score: float, pos: int, neg: int) -> str:
        """生成情绪摘要"""
        if score > 0.3:
            return f"偏利好情绪（正向词{pos}个，负向词{neg}个）"
        elif score < -0.3:
            return f"偏利空情绪（正向词{pos}个，负向词{neg}个）"
        elif pos > 0 or neg > 0:
            return f"中性偏震荡（正向词{pos}个，负向词{neg}个）"
        return "中性情绪"
