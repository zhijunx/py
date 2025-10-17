"""
schedule: 用于定时安排任务。
plyer: 用于发送跨平台的桌面通知（Windows, macOS, Linux 均可用）。
pip install schedule plyer
"""

import schedule
import time
import sys
from plyer import notification

# --- 配置提醒内容 ---

# 设置提醒间隔（分钟）
REMIND_INTERVAL_MINUTES = 1

def water_break_reminder():
    """发送喝水休息提醒的桌面通知"""
    notification_title = "💧 休息时间到！"
    notification_message = "起来走动一下，放松眼睛，补充水分。保持健康，提高效率！"

    print(f"[{time.strftime('%H:%M:%S')}] 发送提醒：{notification_title}")

    # 使用 plyer 发送通知
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name='健康提醒小助手',
        # icon='path/to/icon.ico' # 可选：设置一个自定义图标
        timeout=10  # 通知显示的时间（秒）
    )

def main():
    """主程序：设置定时任务并循环运行"""

    print("====================================================")
    print("⏰ 健康提醒小助手已启动！")
    print(f"   提醒频率：每 {REMIND_INTERVAL_MINUTES} 分钟提醒一次。")
    print("   程序将持续运行，请勿关闭此窗口。")
    print("   按 Ctrl+C 随时退出。")
    print("====================================================")

    # 安排任务：每隔 N 分钟执行一次 water_break_reminder 函数
    # 注意：schedule 库是基于时间间隔运行的，如果需要精确到每天某个时间点，可以使用 .at()
    schedule.every(REMIND_INTERVAL_MINUTES).minutes.do(water_break_reminder)

    try:
        while True:
            # 检查所有待执行的定时任务
            schedule.run_pending()
            # 暂停 1 秒，减少 CPU 占用
            time.sleep(1)

    except KeyboardInterrupt:
        # 用户按下 Ctrl+C 退出程序
        print("\n程序已收到退出指令。")
        sys.exit()

if __name__ == "__main__":
    main()