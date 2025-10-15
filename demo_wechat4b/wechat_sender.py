# only test wechat
# 安装所需库
# pip install PyYAML
# pip install pytest
# pip install requests

# DOC REF
# https://www.runoob.com/w3cnote/yaml-intro.html
# https://www.runoob.com/python3/python3-tutorial.html


import requests
import json
import yaml
import time
import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

def load_config(config_path: str = "demo_wechat4b/config.yaml") -> dict:
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        if config is None:
            return {}
        return config
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"YAML 解析错误: {e}")
    except Exception as e:
        raise Exception(f"加载配置失败: {e}")

def send_wechat_message(webhook_url, msg):
    msg_type = "text"
    if msg_type == "text":
        data = {
            "msgtype": "text",
            "text": {
                "content": msg
            }
        }
    elif msg_type == "markdown":
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": msg
            }
        }
    else:
        print(f"不支持的消息类型: {msg_type}")
        return False

    try:
        headers = {'Content-Type': 'application/json'}
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

def main():

    # 创建东八区时区
    east8 = ZoneInfo('Asia/Shanghai')

    # 获取当前东八区时间
    now_east8 = datetime.now(east8)
    print(f"当前东八区时间: {now_east8}")

    # 格式化输出
    formatted_time = now_east8.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    print(f"格式化时间: {formatted_time}")
    msg = f"""
        {"每日早读"}
        >
        > 时间：{json.dumps(formatted_time, ensure_ascii=False)}
        >
        >10/16 96-98页
        >10/17 98-100页
        """
    # 从环境变量或 secrets 获取 webhook URL
    webhook_url = os.getenv('WECHAT_WEBHOOK_URL')
    if webhook_url:
        print("加载云端config")
    else:
        print("加载本地config")
        config = load_config()
        print(config.get('wechat_work', {}))
        webhook_url = config.get('wechat_work', {}).get('webhook_url')

    success = send_wechat_message(webhook_url, msg)
    sys.exit(0 if success else 1)


# 使用方法二的主函数
if __name__ == "__main__":
    main()