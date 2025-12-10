#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻获取脚本
支持多个新闻源，可定时运行
"""

import requests
from datetime import datetime
import json
import time
from bs4 import BeautifulSoup
import schedule

class NewsAggregator:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_zhihu_hot(self, limit=10):
        """获取知乎热榜"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
            params = {'limit': limit}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            data = response.json()

            news_list = []
            for item in data.get('data', [])[:limit]:
                news_list.append({
                    'title': item['target']['title'],
                    'excerpt': item['target'].get('excerpt', ''),
                    'url': f"https://www.zhihu.com/question/{item['target']['id']}"
                })
            return news_list
        except Exception as e:
            print(f"获取知乎热榜失败: {e}")
            return []

    def get_weibo_hot(self, limit=10):
        """获取微博热搜"""
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()

            news_list = []
            for item in data.get('data', {}).get('realtime', [])[:limit]:
                news_list.append({
                    'title': item.get('note', ''),
                    'hot_value': item.get('num', 0),
                    'url': f"https://s.weibo.com/weibo?q=%23{item.get('word', '')}%23"
                })
            return news_list
        except Exception as e:
            print(f"获取微博热搜失败: {e}")
            return []

    def get_36kr_news(self, limit=10):
        """获取36氪快讯"""
        try:
            url = "https://36kr.com/api/newsflash"
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()

            news_list = []
            for item in data.get('data', {}).get('items', [])[:limit]:
                news_list.append({
                    'title': item.get('title', ''),
                    'summary': item.get('summary', ''),
                    'time': item.get('published_at', ''),
                    'url': f"https://36kr.com/newsflashes/{item.get('id', '')}"
                })
            return news_list
        except Exception as e:
            print(f"获取36氪新闻失败: {e}")
            return []

    def format_news_report(self, zhihu_news, weibo_news, kr_news):
        """格式化新闻报告"""
        report = []
        report.append("=" * 60)
        report.append(f"📰 每日新闻早报 - {datetime.now().strftime('%Y年%m月%d日 %A')}")
        report.append("=" * 60)
        report.append("")

        if zhihu_news:
            report.append("🔥 知乎热榜 TOP 10")
            report.append("-" * 60)
            for i, news in enumerate(zhihu_news, 1):
                report.append(f"{i}. {news['title']}")
                if news['excerpt']:
                    report.append(f"   摘要: {news['excerpt'][:100]}...")
                report.append(f"   链接: {news['url']}")
                report.append("")

        if weibo_news:
            report.append("🔥 微博热搜 TOP 10")
            report.append("-" * 60)
            for i, news in enumerate(weibo_news, 1):
                report.append(f"{i}. {news['title']} (热度: {news['hot_value']})")
                report.append(f"   链接: {news['url']}")
                report.append("")

        if kr_news:
            report.append("💼 36氪快讯")
            report.append("-" * 60)
            for i, news in enumerate(kr_news, 1):
                report.append(f"{i}. {news['title']}")
                if news['summary']:
                    report.append(f"   {news['summary'][:100]}...")
                report.append(f"   时间: {news['time']}")
                report.append("")

        report.append("=" * 60)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)

        return "\n".join(report)

    def save_to_file(self, content, filename=None):
        """保存新闻到文件"""
        if filename is None:
            filename = f"news_{datetime.now().strftime('%Y%m%d')}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 新闻已保存到: {filename}")

    def fetch_daily_news(self):
        """获取每日新闻"""
        print(f"\n⏰ 开始获取新闻... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 获取各平台新闻
        zhihu_news = self.get_zhihu_hot(10)
        time.sleep(1)  # 避免请求过快

        weibo_news = self.get_weibo_hot(10)
        time.sleep(1)

        kr_news = self.get_36kr_news(10)

        # 格式化并保存
        report = self.format_news_report(zhihu_news, weibo_news, kr_news)
        print(report)

        # 保存到文件
        self.save_to_file(report)

        return report

def run_scheduler():
    """运行定时任务"""
    aggregator = NewsAggregator()

    # 设置每天早上8点运行
    schedule.every().day.at("08:00").do(aggregator.fetch_daily_news)

    print("📅 定时任务已启动，每天早上8:00自动获取新闻")
    print("💡 也可以按 Ctrl+C 停止程序")

    # 立即运行一次
    aggregator.fetch_daily_news()

    # 保持运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # 方式1: 立即运行一次
    print("MAIN ENTRY !!!")
    print("选择运行模式:")
    print("1. 立即获取一次新闻")
    print("2. 启动定时任务(每天早上8点)")

    choice = input("请输入选择 (1/2): ").strip()

    aggregator = NewsAggregator()

    if choice == "1":
        aggregator.fetch_daily_news()
    elif choice == "2":
        run_scheduler()
    else:
        print("无效选择，默认立即运行一次")
        aggregator.fetch_daily_news()