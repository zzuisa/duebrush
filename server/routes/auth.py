from flask import Blueprint, request, jsonify
from utils.auth import generate_token, validate_password, validate_token, revoke_token

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

@auth_bp.post('/api/logout')
def logout():
    """管理员登出"""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ', 1)[1].strip()
        revoke_token(token)
    return jsonify({"success": True, "message": "Logged out successfully"})

@auth_bp.get('/api/verify-token')
def verify_token():
    """验证token是否有效"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"success": False, "message": "No token provided"}), 401
    
    token = auth_header.split(' ', 1)[1].strip()
    if validate_token(token):
        return jsonify({"success": True, "message": "Token is valid"})
    else:
        return jsonify({"success": False, "message": "Invalid token"}), 401

@auth_bp.get('/api/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok"})
