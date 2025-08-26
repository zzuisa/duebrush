from flask import Blueprint, request, jsonify
from utils.auth import require_auth
from utils.email import validate_email, send_notification_email, test_email_config
from models.contact import ContactModel

contacts_bp = Blueprint('contacts', __name__)

@contacts_bp.post('/api/contact')
def contact():
    """提交联系表单"""
    print(f"[DEBUG] 收到联系表单请求")
    print(f"[DEBUG] 请求方法: {request.method}")
    print(f"[DEBUG] 请求头: {dict(request.headers)}")
    print(f"[DEBUG] 请求IP: {request.remote_addr}")
    
    payload = request.get_json(silent=True) or request.form.to_dict()
    print(f"[DEBUG] 请求数据: {payload}")
    
    # 验证必填字段
    name = payload.get('name', '').strip()
    email = payload.get('email', '').strip()
    message = payload.get('message', '').strip()
    
    print(f"[DEBUG] 验证字段:")
    print(f"  - 姓名: '{name}' (长度: {len(name)})")
    print(f"  - 邮箱: '{email}' (长度: {len(email)})")
    print(f"  - 消息: '{message}' (长度: {len(message)})")
    
    if not name:
        print(f"[DEBUG] ❌ 姓名验证失败")
        return jsonify({"success": False, "message": "Name is required"}), 400
    if not email:
        print(f"[DEBUG] ❌ 邮箱验证失败")
        return jsonify({"success": False, "message": "Email is required"}), 400
    if not message:
        print(f"[DEBUG] ❌ 消息验证失败")
        return jsonify({"success": False, "message": "Message content is required"}), 400
    
    # 验证邮箱格式
    print(f"[DEBUG] 验证邮箱格式...")
    if not validate_email(email):
        print(f"[DEBUG] ❌ 邮箱格式验证失败")
        return jsonify({"success": False, "message": "Invalid email format"}), 400
    print(f"[DEBUG] ✅ 邮箱格式验证通过")
    
    # 添加IP地址
    contact_data = {
        'name': name,
        'email': email,
        'message': message,
        'ip': request.remote_addr
    }
    print(f"[DEBUG] 准备保存联系数据: {contact_data}")
    
    # 保存联系记录
    try:
        ContactModel.create(contact_data)
        print(f"[DEBUG] ✅ 联系数据保存成功")
    except Exception as e:
        print(f"[DEBUG] ❌ 联系数据保存失败: {e}")
        return jsonify({"success": False, "message": "Failed to save contact data"}), 500
    
    # 发送通知邮件
    print(f"[DEBUG] 开始发送通知邮件...")
    email_sent = send_notification_email(contact_data)
    print(f"[DEBUG] 邮件发送结果: {email_sent}")
    
    response_data = {
        "success": True, 
        "message": "Message sent successfully! We will get back to you soon.",
        "email_sent": email_sent
    }
    print(f"[DEBUG] 返回响应: {response_data}")
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
        return jsonify({"error": "Not Found"}), 404
    
    return jsonify({"success": True, "deleted": deleted_contact})

@contacts_bp.post('/api/test-email')
def test_email():
    """测试邮件配置的API端点"""
    print(f"[DEBUG] 收到邮件测试请求")
    result = test_email_config()
    return jsonify({
        "success": result,
        "message": "Email configuration test completed",
        "test_result": result
    })
