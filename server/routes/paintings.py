from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from models.painting import PaintingModel

paintings_bp = Blueprint('paintings', __name__)

@paintings_bp.get('/api/paintings')
def list_paintings():
    """获取所有绘画列表"""
    paintings = PaintingModel.load_paintings()
    return jsonify(paintings)

@paintings_bp.post('/api/paintings')
@require_auth
def create_painting():
    """创建新绘画"""
    payload = request.get_json(silent=True) or {}
    new_painting = PaintingModel.create(payload)
    return jsonify(new_painting), 201

@paintings_bp.get('/api/paintings/<int:pid>')
def get_painting(pid):
    """获取单个绘画"""
    painting = PaintingModel.get_by_id(pid)
    if not painting:
        return jsonify({"success": False, "message": "Painting not found"}), 404
    return jsonify(painting)

@paintings_bp.put('/api/paintings/<int:pid>')
@paintings_bp.patch('/api/paintings/<int:pid>')
@require_auth
def update_painting(pid):
    """更新绘画"""
    payload = request.get_json(silent=True) or {}
    updated_painting = PaintingModel.update(pid, payload)
    if not updated_painting:
        return jsonify({"success": False, "message": "Painting not found"}), 404
    return jsonify(updated_painting)

@paintings_bp.delete('/api/paintings/<int:pid>')
@require_auth
def delete_painting(pid):
    """删除绘画"""
    if PaintingModel.delete(pid):
        return jsonify({"success": True, "message": "Painting deleted", "id": pid})
    return jsonify({"success": False, "message": "Painting not found"}), 404
