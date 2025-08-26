from flask import Blueprint, request, jsonify, send_from_directory
from utils.auth import require_auth
from utils.file_utils import generate_unique_filename
from config import Config

uploads_bp = Blueprint('uploads', __name__)

@uploads_bp.post('/api/upload')
@require_auth
def upload_file():
    """文件上传"""
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "Empty filename"}), 400
    
    # 确定目标文件名
    raw_client_name = request.form.get('filename', '').strip()
    filename = generate_unique_filename(file.filename, raw_client_name)
    
    # 保存文件
    save_path = Config.UPLOADS_DIR / filename
    file.save(str(save_path))
    
    url_path = f"/uploads/{filename}"
    return jsonify({
        "success": True, 
        "url": url_path, 
        "path": url_path, 
        "filename": filename
    })

@uploads_bp.get('/uploads/<path:filename>')
def serve_upload(filename):
    """提供上传文件服务"""
    return send_from_directory(str(Config.UPLOADS_DIR), filename)
