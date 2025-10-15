# only test wechat
# 安装所需库
# pip install PyYAML
# pip install pytest

# DOC REF
# https://www.runoob.com/w3cnote/yaml-intro.html
# https://www.runoob.com/python3/python3-tutorial.html

import os
import requests
import argparse
import json
import yaml
import time
import sys
import threading
from pathlib import Path
from datetime import datetime

def load_config(config_path: str = "config.yaml") -> dict:
    """
    加载配置文件

    Args:
        config_path (str): 配置文件路径

    Returns:
        dict: 配置信息
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"配置文件 {config_path} 不存在")
        return {}

def send_wechat_alert(webhook_url: str, title: str, content: str, alert_level: str = "info") -> bool:
    """
    发送企业微信告警消息

    Args:
        webhook_url (str): Webhook地址
        title (str): 消息标题
        content (str): 消息内容
        alert_level (str): 告警级别 (info, warning, error)

    Returns:
        bool: 发送是否成功
    """
    # 根据告警级别设置颜色
    color_map = {
        "info": "info",
        "warning": "warning",
        "error": "danger"
    }
    color = color_map.get(alert_level, "info")

    markdown_content = f"""
## {title}

> **告警级别：** <font color=\"{color}\">{alert_level.upper()}</font>
> **时间：** {json.dumps(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ensure_ascii=False)}
>
> **详情：**
> {content}
"""

    data = {
        "msgtype": "markdown",
        "markdown": {"content": markdown_content}
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()  # 如果状态码不是200-399，抛出HTTPError异常
        result = response.json()
        if result.get('errcode') == 0:
            print("消息发送成功")
            return True
        else:
            print(f"业务逻辑失败: errcode={result.get('errcode')}, errmsg={result.get('errmsg')}")
            return False

    except requests.exceptions.Timeout:
        print("请求超时")
        return False
    except requests.exceptions.ConnectionError:
        print("网络连接错误")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"HTTP错误: {e}")
        return False
    except json.JSONDecodeError:
        print("响应JSON解析失败")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False

class WeChatAutoSender:
    def __init__(self, webhook_url: str, interval: int = 30):
        self.webhook_url = webhook_url
        self.interval = interval
        self.is_paused = False
        self.counter = 0
        self.running = True

    def pause(self):
        """暂停发送"""
        if not self.is_paused:
            self.is_paused = True
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 已暂停发送消息")

    def resume(self):
        """恢复发送"""
        if self.is_paused:
            self.is_paused = False
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 已恢复发送消息")

    def toggle_pause(self):
        """切换暂停状态"""
        self.is_paused = not self.is_paused
        status = "已暂停" if self.is_paused else "已恢复"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status}发送消息")

    def stop(self):
        """停止程序"""
        self.running = False
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 正在停止程序...")

    def run(self):
        """运行自动发送"""
        print(f"开始自动发送消息，间隔: {self.interval}秒")
        print("输入 'p' 暂停/恢复发送，输入 'q' 退出程序")

        while self.running:
            if self.is_paused:
                time.sleep(1)
                continue

            self.counter += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 构建消息内容
            title = f"定时监控报告 #{self.counter}"
            content = f"""
这是第 {self.counter} 次定时报告
发送时间: {current_time}
间隔时间: {self.interval}秒
系统运行正常，持续监控中...
"""

            # 发送消息
            success = send_wechat_alert(
                self.webhook_url,
                title,
                content,
                "info"
            )

            if success:
                print(f"[{current_time}] 第 {self.counter} 次消息发送成功，等待 {self.interval} 秒后继续...")
            else:
                print(f"[{current_time}] 第 {self.counter} 次消息发送失败，等待 {self.interval} 秒后重试...")

            # 等待指定间隔，支持在等待期间响应暂停
            wait_time = self.interval
            while wait_time > 0 and self.running:
                time.sleep(1)
                wait_time -= 1
                if self.is_paused:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 发送已暂停，剩余等待时间: {wait_time}秒")
                    while self.is_paused and self.running:
                        time.sleep(1)

def send_wechat_message(webhook_url, message, msg_type="text"):
    """
    发送企业微信消息

    Args:
        webhook_url: 企业微信机器人 webhook URL
        message: 消息内容
        msg_type: 消息类型 (text/markdown)
    """
    if msg_type == "text":
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
    elif msg_type == "markdown":
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": message
            }
        }
    else:
        print(f"不支持的消息类型: {msg_type}")
        return False

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            webhook_url,
            data=json.dumps(data),
            headers=headers,
            timeout=10
        )

        result = response.json()
        if result.get('errcode') == 0:
            print("✅ 消息发送成功")
            return True
        else:
            print(f"❌ 消息发送失败: {result.get('errmsg')}")
            return False

    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='发送企业微信消息')
    parser.add_argument('--content', type=str, required=True, help='消息内容')
    parser.add_argument('--type', type=str, choices=['text', 'markdown'], default='text', help='消息类型')

    args = parser.parse_args()

    # 从环境变量或 secrets 获取 webhook URL
    webhook_url = os.getenv('WECHAT_WEBHOOK_URL')
    if not webhook_url:
        print("❌ 请设置 WECHAT_WEBHOOK_URL 环境变量")
        sys.exit(1)

    success = send_wechat_message(webhook_url, args.content, args.type)
    sys.exit(0 if success else 1)


# 使用方法二的主函数
if __name__ == "__main__":
    main()