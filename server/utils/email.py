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
    if not Config.SMTP_USERNAME or not Config.SMTP_PASSWORD:
        return False
    
    try:
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
        
        # 根据端口选择连接方式
        if Config.SMTP_PORT == 465:
            # 使用SSL连接
            server = smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT)
        else:
            # 使用TLS连接
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
        
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        return False

def test_email_config():
    """测试邮件配置"""
    if not Config.SMTP_USERNAME or not Config.SMTP_PASSWORD:
        return False
    
    try:
        # 根据端口选择连接方式
        if Config.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT)
        else:
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
        
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        
        test_msg = MIMEMultipart()
        test_msg['From'] = Config.SMTP_USERNAME
        test_msg['To'] = Config.ADMIN_EMAIL
        test_msg['Subject'] = "Email Configuration Test"
        test_msg.attach(MIMEText("This is a test email to verify configuration.", 'plain', 'utf-8'))
        
        server.send_message(test_msg)
        server.quit()
        
        return True
        
    except Exception as e:
        return False
