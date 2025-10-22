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
import os
import sys
import datetime
from zoneinfo import ZoneInfo

def load_config(config_path: str = "config.yaml") -> dict:
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
    msg_type = "markdown"
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
    now_east8 = datetime.datetime.now(east8)
    print(f"当前东八区时间: {now_east8}")

    # 格式化输出
    formatted_time = now_east8.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    print(f"格式化时间: {formatted_time}")

    # --- 1. 定义 ANSI 转义序列 ---
    # 红色 (RED: \033[91m 或 \033[31m)
    # 加粗 (BOLD: \033[1m)
    # 结束所有格式 (END: \033[0m)
    # RED_BOLD_START = '\033[1;91m' # 1 for BOLD, 91 for bright RED
    # END = '\033[0m'
    WARNING_BOLD_START = '<font color="warning">**'
    END = '**</font>'

    # 如果在 Windows 终端上遇到问题，可以尝试导入 colorama
    # from colorama import init, Fore, Style
    # init(autoreset=True)
    # RED_BOLD_START = Style.BRIGHT + Fore.RED
    # END = Style.RESET_ALL

    # --- 2. 获取当前日期并格式化 ---
    # 获取系统当前日期 (年-月-日)
    today = datetime.date.today()
    # 格式化为 "MM月DD日"，例如 "10月22日"
    # %-m（或%#m在Windows上）去除月份前的0，但为了兼容性，我们手动处理
    chinese_date_format = f"{today.month}月{today.day}日"

    msg = f"""
        每日早读
        时间：{json.dumps(formatted_time, ensure_ascii=False)}
        日期 读书内容 页数
        10月20日 人类交往中有一条核心法则 默默无闻中死 100-101
        10月21日 这就是发自内心 老爷车聊表谢意 102-104
        10月22日 不管你多么显要 是他参与设计的 104-106
        10月23日 两个人边走边欣赏 多么神奇的效果 106-108
        10月24日 第三部分 服务也非常好 109-111
        10月27日 他一下子就不知道 伤口也不会好 112-113
        10月28日 新泽西州费尔菲尔 赢得争论的唯一方式就是避免争论　 114-115
        10月29日 尊重他人的想法 法律常识错误 116-118
        10月30日 绝对客观公正 固执已见的行为 118-120
        10月31日 我给自己定了规矩 培训课上学到的原则 120-121
        11月3日 当我到达工厂时永远不要对他说“你错了 122-123
        11月4日 主动真诚地承认错误 对此我感到很抱歉， 124-126
        11月5日 听了我的话　化敌为友 126-127
        11月6日 例如没有人不满和惯惯不平 128-130
        11月7日 丹尼尔·韦佰斯特是美国避免公司陷入，尴尬境地 130-131
        """
    # --- 4. 遍历并格式化输出 ---
    lines = msg.strip().split('\n')
    output_lines = []
    output_lines.append(f"       **{lines[0].strip()}**")
    for line in lines[1:]:
        stripped_line = line.strip()
        if chinese_date_format in stripped_line:
            formatted_line = f"{WARNING_BOLD_START}{line}{END}"
        else:
            formatted_line = line
        output_lines.append(formatted_line)
    final_msg = '\n'.join(output_lines)

    # print(final_msg)
    # 从环境变量或 secrets 获取 webhook URL
    webhook_url = os.getenv('WECHAT_WEBHOOK_URL')
    if webhook_url:
        print("加载云端config")
    else:
        print("加载本地config")
        config = load_config()
        print(config.get('wechat_work', {}))
        webhook_url = config.get('wechat_work', {}).get('webhook_url')
    success = send_wechat_message(webhook_url, final_msg)
    sys.exit(0 if success else 1)

# 使用方法二的主函数
if __name__ == "__main__":
    main()