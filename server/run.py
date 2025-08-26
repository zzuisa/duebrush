#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后端应用主运行文件
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    # Flask 3.0.3 + Werkzeug 3 支持 reloader_type='stat'，避免监听非代码文件（如 uploads）
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
