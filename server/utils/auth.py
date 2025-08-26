import secrets
from functools import wraps
from flask import request, jsonify
from config import Config

# 活跃的认证令牌集合
active_tokens = set()

def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(' ', 1)[1].strip()
        if token not in active_tokens:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return wrapper

def generate_token():
    """生成新的认证令牌"""
    token = secrets.token_urlsafe(24)
    active_tokens.add(token)
    return token

def validate_token(token):
    """验证令牌是否有效"""
    return token in active_tokens

def revoke_token(token):
    """撤销令牌"""
    active_tokens.discard(token)

def validate_password(password):
    """验证管理员密码"""
    return password == Config.ADMIN_PASSWORD
