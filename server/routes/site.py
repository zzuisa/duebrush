from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from models.site import SiteModel

site_bp = Blueprint('site', __name__)

# 轮播图相关路由
@site_bp.get('/api/slider')
def get_slider():
    """获取轮播图数据"""
    slider = SiteModel.get_slider()
    return jsonify(slider)

@site_bp.post('/api/slider')
@require_auth
def set_slider():
    """设置轮播图数据"""
    payload = request.get_json(silent=True) or []
    if not isinstance(payload, list):
        return jsonify({"success": False, "message": "Expect list"}), 400
    
    SiteModel.set_slider(payload)
    return jsonify({"success": True})

# 作者相关路由
@site_bp.get('/api/authors')
def get_authors():
    """获取作者列表"""
    authors = SiteModel.get_authors()
    return jsonify(authors)

@site_bp.post('/api/authors')
@require_auth
def create_author():
    """创建新作者"""
    payload = request.get_json(silent=True) or {}
    new_author = SiteModel.create_author(payload)
    return jsonify(new_author), 201

@site_bp.get('/api/authors/<int:aid>')
def get_author(aid):
    """获取单个作者"""
    author = SiteModel.get_author_by_id(aid)
    if not author:
        return jsonify({"success": False, "message": "Author not found"}), 404
    return jsonify(author)

@site_bp.put('/api/authors/<int:aid>')
@site_bp.patch('/api/authors/<int:aid>')
@require_auth
def update_author(aid):
    """更新作者信息"""
    payload = request.get_json(silent=True) or {}
    updated_author = SiteModel.update_author(aid, payload)
    if not updated_author:
        return jsonify({"success": False, "message": "Author not found"}), 404
    return jsonify(updated_author)

@site_bp.delete('/api/authors/<int:author_id>')
@require_auth
def delete_author(author_id):
    """删除作者"""
    if SiteModel.delete_author(author_id):
        return jsonify({"success": True, "message": "Author deleted", "id": author_id})
    return jsonify({"success": False, "message": "Author not found"}), 404

# 向后兼容的单个作者API
@site_bp.get('/api/author')
def get_author_legacy():
    """获取第一个作者（向后兼容）"""
    author = SiteModel.get_first_author()
    return jsonify(author)

@site_bp.post('/api/author')
@require_auth
def set_author_legacy():
    """设置第一个作者（向后兼容）"""
    payload = request.get_json(silent=True) or {}
    author = SiteModel.set_first_author(payload)
    return jsonify({"success": True, "author": author})
