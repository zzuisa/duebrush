from flask import Blueprint, request, jsonify
from utils.auth import generate_token, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/api/login')
def login():
    """管理员登录"""
    payload = request.get_json(silent=True) or {}
    password = payload.get('password')
    
    if not password:
        return jsonify({"success": False, "message": "Password required"}), 400
    
    if not validate_password(password):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    
    token = generate_token()
    return jsonify({"success": True, "token": token})

@auth_bp.get('/api/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok"})
