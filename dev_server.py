#!/usr/bin/env python3
"""
开发环境启动脚本
用于本地开发调试
"""

import os
import sys
from pathlib import Path

# 添加server目录到Python路径
server_dir = Path(__file__).parent / 'server'
sys.path.insert(0, str(server_dir))

# 设置开发环境变量
os.environ['FLASK_ENV'] = 'development'
os.environ['ADMIN_PASSWORD'] = 'dev2025'  # 开发环境密码

# 导入并启动Flask应用
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("🚀 开发服务器启动中...")
    print("📍 管理后台: http://localhost:5000/admin/")
    print("🌐 前端页面: http://localhost:5000/")
    print("🔑 开发密码: dev2025")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True, 
        use_reloader=True
    )
