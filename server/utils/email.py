import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def send_notification_email(contact_data):
    """发送通知邮件给管理员"""
    print(f"[DEBUG] 开始邮件发送流程...")
    print(f"[DEBUG] 配置信息:")
    print(f"  - SMTP服务器: {Config.SMTP_SERVER}")
    print(f"  - SMTP端口: {Config.SMTP_PORT}")
    print(f"  - 发件人邮箱: {Config.SMTP_USERNAME}")
    print(f"  - 收件人邮箱: {Config.ADMIN_EMAIL}")
    print(f"  - 密码配置: {'已配置' if Config.SMTP_PASSWORD else '未配置'}")
    
    if not Config.SMTP_USERNAME or not Config.SMTP_PASSWORD:
        print(f"[DEBUG] ❌ 邮件配置不完整，跳过发送")
        return False
    
    try:
        print(f"[DEBUG] 创建邮件内容...")
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = Config.ADMIN_EMAIL
        msg['Subject'] = f"New Contact Form Message - {contact_data.get('name', 'Anonymous')}"
        
        body = f"""
        New contact form message received:
        
        Name: {contact_data.get('name', 'Not provided')}
        Email: {contact_data.get('email', 'Not provided')}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Message:
        {contact_data.get('message', 'No content')}
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        print(f"[DEBUG] 邮件内容创建完成")
        print(f"[DEBUG] 邮件主题: {msg['Subject']}")
        print(f"[DEBUG] 邮件正文长度: {len(body)} 字符")
        
        print(f"[DEBUG] 连接SMTP服务器...")
        
        # 根据端口选择连接方式
        if Config.SMTP_PORT == 465:
            # 使用SSL连接
            print(f"[DEBUG] 使用SSL连接 (端口465)")
            server = smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT)
        else:
            # 使用TLS连接
            print(f"[DEBUG] 使用TLS连接 (端口587)")
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            print(f"[DEBUG] 启动TLS加密...")
            server.starttls()
        
        print(f"[DEBUG] SMTP连接成功")
        
        print(f"[DEBUG] 尝试登录...")
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        print(f"[DEBUG] 登录成功")
        
        print(f"[DEBUG] 发送邮件...")
        server.send_message(msg)
        print(f"[DEBUG] 邮件发送成功")
        
        print(f"[DEBUG] 关闭连接...")
        server.quit()
        print(f"[DEBUG] 连接已关闭")
        
        print(f"[DEBUG] ✅ 邮件发送流程完成")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"[DEBUG] ❌ SMTP认证失败: {e}")
        print(f"[DEBUG] 请检查邮箱和密码是否正确")
        return False
    except smtplib.SMTPRecipientsRefused as e:
        print(f"[DEBUG] ❌ 收件人拒绝: {e}")
        print(f"[DEBUG] 请检查收件人邮箱地址是否正确")
        return False
    except smtplib.SMTPSenderRefused as e:
        print(f"[DEBUG] ❌ 发件人拒绝: {e}")
        print(f"[DEBUG] 请检查发件人邮箱地址是否正确")
        return False
    except smtplib.SMTPDataError as e:
        print(f"[DEBUG] ❌ 邮件数据错误: {e}")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"[DEBUG] ❌ SMTP连接错误: {e}")
        print(f"[DEBUG] 请检查SMTP服务器地址和端口是否正确")
        return False
    except smtplib.SMTPHeloError as e:
        print(f"[DEBUG] ❌ SMTP HELO错误: {e}")
        return False
    except smtplib.SMTPNotSupportedError as e:
        print(f"[DEBUG] ❌ SMTP不支持的操作: {e}")
        return False
    except Exception as e:
        print(f"[DEBUG] ❌ 未知错误: {e}")
        print(f"[DEBUG] 错误类型: {type(e).__name__}")
        return False

def test_email_config():
    """测试邮件配置"""
    print(f"[DEBUG] 开始测试邮件配置...")
    Config.print_config()
    
    if not Config.SMTP_USERNAME or not Config.SMTP_PASSWORD:
        print(f"[DEBUG] ❌ 邮件配置不完整")
        return False
    
    try:
        print(f"[DEBUG] 测试SMTP连接...")
        
        # 根据端口选择连接方式
        if Config.SMTP_PORT == 465:
            print(f"[DEBUG] 使用SSL连接 (端口465)")
            server = smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT)
        else:
            print(f"[DEBUG] 使用TLS连接 (端口587)")
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            print(f"[DEBUG] 测试TLS...")
            server.starttls()
        
        print(f"[DEBUG] SMTP连接成功")
        
        print(f"[DEBUG] 测试登录...")
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        print(f"[DEBUG] 登录成功")
        
        print(f"[DEBUG] 测试发送测试邮件...")
        test_msg = MIMEMultipart()
        test_msg['From'] = Config.SMTP_USERNAME
        test_msg['To'] = Config.ADMIN_EMAIL
        test_msg['Subject'] = "Email Configuration Test"
        test_msg.attach(MIMEText("This is a test email to verify configuration.", 'plain', 'utf-8'))
        
        server.send_message(test_msg)
        print(f"[DEBUG] 测试邮件发送成功")
        
        server.quit()
        print(f"[DEBUG] ✅ 邮件配置测试通过")
        return True
        
    except Exception as e:
        print(f"[DEBUG] ❌ 邮件配置测试失败: {e}")
        return False
