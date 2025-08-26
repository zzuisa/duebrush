#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
邮件发送测试
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_env_loading():
    """测试.env文件加载"""
    print("🔍 测试.env文件加载")
    print("=" * 40)
    
    # 加载.env文件
    from dotenv import load_dotenv
    load_dotenv()
    
    # 检查环境变量
    env_vars = {
        'SMTP_SERVER': os.getenv('SMTP_SERVER'),
        'SMTP_PORT': os.getenv('SMTP_PORT'),
        'SMTP_USERNAME': os.getenv('SMTP_USERNAME'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL'),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD')
    }
    
    print("环境变量检查结果:")
    for var, value in env_vars.items():
        if value:
            if 'PASSWORD' in var:
                print(f"  {var}: {'*' * len(value)}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: 未设置")
    
    # 检查关键变量
    required_vars = ['SMTP_USERNAME', 'SMTP_PASSWORD', 'ADMIN_EMAIL']
    missing_vars = [var for var in required_vars if not env_vars[var]]
    
    if missing_vars:
        print(f"\n❌ 缺少关键环境变量: {', '.join(missing_vars)}")
        return False
    else:
        print(f"\n✅ 所有关键环境变量都已设置")
        return True

def test_email_config():
    """测试邮件配置"""
    print("\n" + "=" * 50)
    print("邮件配置测试")
    print("=" * 50)
    
    try:
        from config import Config
        
        print(f"SMTP服务器: {Config.SMTP_SERVER}")
        print(f"SMTP端口: {Config.SMTP_PORT}")
        print(f"发件人邮箱: {Config.SMTP_USERNAME}")
        print(f"收件人邮箱: {Config.ADMIN_EMAIL}")
        print(f"密码配置: {'已配置' if Config.SMTP_PASSWORD else '未配置'}")
        
        if not Config.SMTP_USERNAME or not Config.SMTP_PASSWORD:
            print("❌ 邮件配置不完整，请设置环境变量:")
            print("  - SMTP_USERNAME: 发件人邮箱")
            print("  - SMTP_PASSWORD: 邮箱密码或应用专用密码")
            return False
        
        print("✅ 配置检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_email_sending():
    """测试邮件发送"""
    print("\n" + "=" * 50)
    print("邮件发送测试")
    print("=" * 50)
    
    try:
        from utils.email import test_email_config
        
        result = test_email_config()
        if result:
            print("✅ 邮件发送测试成功")
        else:
            print("❌ 邮件发送测试失败")
        return result
        
    except Exception as e:
        print(f"❌ 邮件发送测试异常: {e}")
        return False

def test_contact_form():
    """测试联系表单流程"""
    print("\n" + "=" * 50)
    print("联系表单流程测试")
    print("=" * 50)
    
    try:
        from utils.email import send_notification_email
        
        # 模拟联系表单数据
        test_contact_data = {
            'name': '测试用户',
            'email': 'test@example.com',
            'message': '这是一条测试消息',
            'ip': '127.0.0.1',
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"测试数据: {test_contact_data}")
        
        result = send_notification_email(test_contact_data)
        if result:
            print("✅ 联系表单邮件发送成功")
        else:
            print("❌ 联系表单邮件发送失败")
        return result
        
    except Exception as e:
        print(f"❌ 联系表单测试异常: {e}")
        return False

def main():
    """主函数"""
    print("邮件发送调试工具")
    print("=" * 50)
    
    # 测试环境变量加载
    env_ok = test_env_loading()
    if not env_ok:
        print("\n❌ 环境变量测试失败")
        return
    
    # 测试配置
    config_ok = test_email_config()
    if not config_ok:
        print("\n❌ 配置测试失败，请检查环境变量设置")
        return
    
    # 测试邮件发送
    email_ok = test_email_sending()
    if not email_ok:
        print("\n❌ 邮件发送测试失败，请检查邮箱配置")
        return
    
    # 测试联系表单
    contact_ok = test_contact_form()
    if not contact_ok:
        print("\n❌ 联系表单测试失败")
        return
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)

if __name__ == "__main__":
    main()
