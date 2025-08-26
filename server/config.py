import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Config:
    """应用配置类"""
    
    # 基础路径配置
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / 'data'
    UPLOADS_DIR = BASE_DIR / 'uploads'
    
    # 数据文件路径
    PAINTINGS_FILE = DATA_DIR / 'paintings.json'
    CONTACTS_FILE = DATA_DIR / 'contacts.jsonl'
    SITE_FILE = DATA_DIR / 'site.json'
    
    # 认证配置
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'brush2025')
    
    # 邮件配置
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))  # 默认使用587端口
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'zzuisa.cn@gmail.com')
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    @classmethod
    def init_dirs(cls):
        """初始化必要的目录"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def print_config(cls):
        """打印当前配置信息（用于调试）"""
        print("=" * 50)
        print("当前邮件配置:")
        print(f"SMTP服务器: {cls.SMTP_SERVER}")
        print(f"SMTP端口: {cls.SMTP_PORT}")
        print(f"发件人邮箱: {cls.SMTP_USERNAME}")
        print(f"收件人邮箱: {cls.ADMIN_EMAIL}")
        print(f"密码配置: {'已配置' if cls.SMTP_PASSWORD else '未配置'}")
        print("=" * 50)
