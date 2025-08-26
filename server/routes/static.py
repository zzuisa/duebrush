from flask import Blueprint, send_from_directory, jsonify
from pathlib import Path
from config import Config

static_bp = Blueprint('static', __name__)

@static_bp.get('/')
def serve_index():
    """服务首页"""
    return send_from_directory(str(Config.BASE_DIR.parent), 'index.html')

@static_bp.get('/admin/')
@static_bp.get('/admin')
def serve_admin():
    """服务管理页面"""
    return send_from_directory(str(Config.BASE_DIR.parent / 'admin'), 'index.html')

@static_bp.get('/admin/login')
def serve_admin_login():
    """服务管理登录页面"""
    return send_from_directory(str(Config.BASE_DIR.parent / 'admin'), 'login.html')

@static_bp.get('/<path:filename>')
def serve_static(filename):
    """服务静态文件"""
    # 静态文件路径
    static_paths = [
        Config.BASE_DIR.parent / '_include',
        Config.BASE_DIR.parent
    ]
    
    for static_path in static_paths:
        file_path = static_path / filename
        if file_path.exists() and file_path.is_file():
            return send_from_directory(str(static_path), filename)
    
    # 如果文件不存在，返回404
    return jsonify({"error": "Not Found"}), 404
