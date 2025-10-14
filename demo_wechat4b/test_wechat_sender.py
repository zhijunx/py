import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wechat_sender import load_config, WeChatAutoSender

def test_load_config():
    """测试配置文件加载"""
    # 测试文件不存在的情况
    config = load_config("non_existent.yaml")
    assert config == {}

def test_wechat_sender_initialization():
    """测试WeChatAutoSender类初始化"""
    sender = WeChatAutoSender("test_webhook", 30)
    assert sender.webhook_url == "test_webhook"
    assert sender.interval == 30
    assert sender.is_paused == False
    assert sender.counter == 0
    assert sender.running == True

def test_pause_resume():
    """测试暂停和恢复功能"""
    sender = WeChatAutoSender("test_webhook", 30)

    # 测试暂停
    sender.pause()
    assert sender.is_paused == True

    # 测试恢复
    sender.resume()
    assert sender.is_paused == False

    # 测试切换
    sender.toggle_pause()
    assert sender.is_paused == True
    sender.toggle_pause()
    assert sender.is_paused == False

def test_stop():
    """测试停止功能"""
    sender = WeChatAutoSender("test_webhook", 30)
    sender.stop()
    assert sender.running == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])