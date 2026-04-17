"""
FinBuddy CLI - 命令行界面
提供交互式命令行工具，支持情绪分析、公告摘要、财务报告等功能
"""

import sys
import json
import argparse
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from . import __version__
from .analyzer import SentimentAnalyzer
from .summarizer import AnnouncementSummarizer
from .reporter import FinancialReporter
from .client import FinBuddyClient

console = Console()


def _safe_print(text: str):
    """安全打印，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))


def sentiment_command(args):
    """情绪分析命令"""
    analyzer = SentimentAnalyzer()
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = console.input("\n[bold green]请输入要分析的文本:[/bold green] ")
    
    result = analyzer.analyze_text(text)
    
    console.print()
    console.print(Panel.fit(
        f"[bold]情绪分析结果[/bold]\n\n"
        f"情绪等级: {result.level.value}\n"
        f"情绪分数: {result.score:.3f} (-1 到 1)\n"
        f"确信度: {result.confidence:.1%}",
        border_style="blue"
    ))
    
    if result.keywords:
        console.print("\n[yellow]关键词:[/yellow]")
        for kw in result.keywords:
            console.print(f"  {kw}")
    
    console.print(f"\n[cyan]摘要:[/cyan] {result.summary}")


def batch_sentiment_command(args):
    """批量情绪分析命令"""
    analyzer = SentimentAnalyzer()
    
    texts = []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
    elif args.json:
        data = json.loads(args.json)
        texts = data if isinstance(data, list) else [data]
    else:
        console.print("[yellow]请提供 --file 或 --json 参数[/yellow]")
        return
    
    results = analyzer.analyze_batch(texts)
    
    table = Table(title="批量情绪分析结果")
    table.add_column("序号", style="cyan", width=4)
    table.add_column("情绪", style="magenta")
    table.add_column("分数", justify="right", width=8)
    table.add_column("摘要", style="green")
    
    for i, r in enumerate(results, 1):
        emoji = {
            "极度乐观": "😄",
            "偏乐观": "🙂",
            "中性": "😐",
            "偏悲观": "😟",
            "极度悲观": "😢"
        }.get(r.level.value, "❓")
        
        table.add_row(
            str(i),
            f"{emoji} {r.level.value}",
            f"{r.score:+.3f}",
            r.summary[:30] + "..." if len(r.summary) > 30 else r.summary
        )
    
    console.print()
    console.print(table)


def announce_command(args):
    """公告摘要命令"""
    summarizer = AnnouncementSummarizer()
    
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = console.input("\n[bold green]请输入公告全文:[/bold green] (输入完成后按Ctrl+D结束)\n")
        text = sys.stdin.read()
    
    title = args.title or "未知标题"
    date = args.date or ""
    
    result = summarizer.parse_announcement(text, title, date)
    
    console.print()
    console.print(Panel.fit(
        f"[bold]公告摘要[/bold]\n\n"
        f"公司: {result.company} ({result.stock_code})\n"
        f"类型: {result.announcement_type}\n"
        f"信号: {result.investment_signal}",
        border_style="green"
    ))
    
    if result.key_points:
        console.print("\n[yellow]关键点:[/yellow]")
        for point in result.key_points:
            console.print(f"  • {point}")
    
    if result.risk_factors:
        console.print("\n[red]风险提示:[/red]")
        for risk in result.risk_factors:
            console.print(f"  ⚠️ {risk}")
    
    console.print(f"\n[cyan]完整摘要:[/cyan]\n{result.summary}")


def financial_command(args):
    """财务报告命令"""
    reporter = FinancialReporter()
    
    # 解析财务数据
    financial_data = {}
    if args.data:
        try:
            financial_data = json.loads(args.data)
        except json.JSONDecodeError:
            # 尝试解析简单格式 key=value,key2=value2
            for pair in args.data.split(','):
                if '=' in pair:
                    k, v = pair.split('=', 1)
                    try:
                        financial_data[k.strip()] = float(v.strip())
                    except ValueError:
                        pass
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            financial_data = json.load(f)
    else:
        console.print("[yellow]请提供财务数据 --data 或 --file[/yellow]")
        return
    
    stock_code = args.code or "000000"
    company_name = args.name or "某公司"
    
    report = reporter.create_report(stock_code, company_name, financial_data)
    
    # 输出格式
    if args.format == "json":
        console.print(reporter.format_json(report))
    elif args.format == "markdown":
        console.print(reporter.format_markdown(report))
    else:
        output = reporter.format_terminal(report)
        for line in output.split('\n'):
            _safe_print(line)


def analyze_command(args):
    """综合分析命令"""
    client = FinBuddyClient()
    
    # 收集数据
    news_texts = []
    if args.news_file:
        with open(args.news_file, 'r', encoding='utf-8') as f:
            news_texts = [line.strip() for line in f if line.strip()]
    
    announcements = []
    if args.ann_file:
        with open(args.ann_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            announcements = data if isinstance(data, list) else [data]
    
    financial_data = {}
    if args.fin_file:
        with open(args.fin_file, 'r', encoding='utf-8') as f:
            financial_data = json.load(f)
    
    # 执行分析
    from .client import StockInfo
    stock = StockInfo(
        code=args.code or "000000",
        name=args.name or "某公司",
        market="SH",
        industry="未知",
        sector="未知"
    )
    
    result = client.comprehensive_analysis(
        stock, news_texts, announcements, financial_data if financial_data else None
    )
    
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]综合分析报告[/bold cyan] - {result.stock.name} ({result.stock.code})",
        border_style="cyan"
    ))
    
    console.print(f"\n[bold]整体信号:[/bold] {result.overall_signal}")
    console.print(f"[bold]分析置信度:[/bold] {result.confidence:.1%}")
    
    if result.sentiment:
        console.print(f"\n[yellow]市场情绪:[/yellow] {result.sentiment.score:+.3f}")
    
    if result.announcements:
        signals = {}
        for ann in result.announcements:
            sig = ann.investment_signal
            signals[sig] = signals.get(sig, 0) + 1
        console.print(f"[yellow]公告信号分布:[/yellow] {signals}")
    
    console.print("\n[green]分析完成![/green]")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="FinBuddy - A股金融情报助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 情绪分析
  finbuddy sentiment --text "某公司业绩大幅增长"
  finbuddy sentiment --file news.txt
  
  # 批量情绪分析
  finbuddy batch-sentiment --file texts.txt
  finbuddy batch-sentiment --json '["利好消息", "利空消息"]'
  
  # 公告摘要
  finbuddy announce --file announcement.txt --title "业绩预告"
  
  # 财务报告
  finbuddy financial --code 600519 --name "贵州茅台" \\
    --data '{"revenue":1200,"profit":600,"eps":48,"roe":30}'
  
  # 综合分析
  finbuddy analyze --code 600519 --name "贵州茅台" \\
    --news-file news.txt --fin-file financial.json
"""
    )
    
    parser.add_argument("--version", "-v", action="version", 
                       version=f"FinBuddy v{__version__}")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # sentiment
    p_sentiment = subparsers.add_parser("sentiment", help="分析文本情绪")
    p_sentiment.add_argument("--text", "-t", help="待分析文本")
    p_sentiment.add_argument("--file", "-f", help="从文件读取文本")
    
    # batch-sentiment
    p_batch = subparsers.add_parser("batch-sentiment", help="批量分析情绪")
    p_batch.add_argument("--file", "-f", help="文本文件，每行一条")
    p_batch.add_argument("--json", "-j", help="JSON数组格式")
    
    # announce
    p_announce = subparsers.add_parser("announce", help="生成公告摘要")
    p_announce.add_argument("--text", "-t", help="公告全文")
    p_announce.add_argument("--file", "-f", help="从文件读取")
    p_announce.add_argument("--title", help="公告标题")
    p_announce.add_argument("--date", help="发布日期 YYYY-MM-DD")
    
    # financial
    p_fin = subparsers.add_parser("financial", help="生成财务报告")
    p_fin.add_argument("--code", help="股票代码")
    p_fin.add_argument("--name", help="公司名称")
    p_fin.add_argument("--data", help="JSON格式财务数据")
    p_fin.add_argument("--file", "-f", help="从JSON文件读取")
    p_fin.add_argument("--format", choices=["terminal", "json", "markdown"],
                      default="terminal", help="输出格式")
    
    # analyze
    p_analyze = subparsers.add_parser("analyze", help="综合分析")
    p_analyze.add_argument("--code", help="股票代码")
    p_analyze.add_argument("--name", help="公司名称")
    p_analyze.add_argument("--news-file", help="新闻文件")
    p_analyze.add_argument("--ann-file", help="公告JSON文件")
    p_analyze.add_argument("--fin-file", help="财务数据JSON文件")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 命令路由
    command_map = {
        "sentiment": sentiment_command,
        "batch-sentiment": batch_sentiment_command,
        "announce": announce_command,
        "financial": financial_command,
        "analyze": analyze_command,
    }
    
    cmd_func = command_map.get(args.command)
    if cmd_func:
        try:
            cmd_func(args)
        except KeyboardInterrupt:
            console.print("\n[yellow]操作已取消[/yellow]")
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
