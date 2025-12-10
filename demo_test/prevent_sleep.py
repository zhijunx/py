import ctypes
import time
import sys

# Windows API常量
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

def prevent_sleep():
    """
    阻止系统进入休眠状态
    ES_CONTINUOUS: 持续生效直到下次调用
    ES_SYSTEM_REQUIRED: 防止系统自动休眠
    ES_DISPLAY_REQUIRED: 防止显示器关闭
    """
    print("正在启动防休眠模式...")
    print("按 Ctrl+C 可以停止程序并恢复正常休眠设置")

    # 设置线程执行状态,阻止系统休眠
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )

    try:
        print("✓ 防休眠模式已激活")
        print("系统将保持唤醒状态,显示器也不会自动关闭")

        # 保持脚本运行
        while True:
            time.sleep(60)  # 每60秒检查一次

    except KeyboardInterrupt:
        print("\n\n正在停止防休眠模式...")
        # 恢复正常的电源管理设置
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("✓ 已恢复正常休眠设置")
        sys.exit(0)

if __name__ == "__main__":
    # 检查是否在Windows系统上运行
    if sys.platform != "win32":
        print("错误: 此脚本仅支持Windows系统")
        sys.exit(1)

    prevent_sleep()