from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from utils.email import validate_email, send_notification_email, test_email_config
from models.contact import ContactModel

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.post('/api/contact')
def contact():
    """提交联系表单"""
    payload = request.get_json(silent=True) or request.form.to_dict()
    
    # 验证必填字段
    name = payload.get('name', '').strip()
    email = payload.get('email', '').strip()
    message = payload.get('message', '').strip()
    
    if not name:
        return jsonify({"success": False, "message": "Name is required"}), 400
    if not email:
        return jsonify({"success": False, "message": "Email is required"}), 400
    if not message:
        return jsonify({"success": False, "message": "Message content is required"}), 400
    
    # 验证邮箱格式
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format"}), 400
    
    # 添加IP地址
    contact_data = {
        'name': name,
        'email': email,
        'message': message,
        'ip': request.remote_addr
    }
    
    # 保存联系记录
    try:
        ContactModel.create(contact_data)
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to save contact data"}), 500
    
    # 发送通知邮件
    email_sent = send_notification_email(contact_data)
    
    response_data = {
        "success": True, 
        "message": "Message sent successfully! We will get back to you soon.",
        "email_sent": email_sent
    }
    return jsonify(response_data)

@contacts_bp.get('/api/contacts')
@require_auth
def get_contacts():
    """获取所有联系记录（需要认证）"""
    contacts = ContactModel.load_contacts()
    return jsonify(contacts)

@contacts_bp.get('/api/contacts/stats')
@require_auth
def get_contact_stats():
    """获取联系表单统计信息"""
    stats = ContactModel.get_stats()
    return jsonify(stats)

@contacts_bp.delete('/api/contacts/<int:contact_id>')
@require_auth
def delete_contact(contact_id):
    """删除特定联系记录"""
    deleted_contact = ContactModel.delete_by_index(contact_id)
    if not deleted_contact:
        return jsonify({"success": False, "message": "Contact not found"}), 404
    
    return jsonify({"success": True, "deleted": deleted_contact})

@contacts_bp.post('/api/test-email')
def test_email():
    """测试邮件配置的API端点"""
    result = test_email_config()
    return jsonify({
        "success": result,
        "message": "Email configuration test completed",
        "test_result": result
    })
