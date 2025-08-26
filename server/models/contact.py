from datetime import datetime
from utils.file_utils import load_jsonl_file, save_jsonl_file, append_jsonl_file
from config import Config

class ContactModel:
    """联系表单数据模型"""
    
    @staticmethod
    def load_contacts():
        """加载所有联系记录"""
        contacts = load_jsonl_file(Config.CONTACTS_FILE)
        # 按时间倒序排列
        contacts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return contacts
    
    @staticmethod
    def create(contact_data):
        """创建新的联系记录"""
        contact_data['timestamp'] = datetime.now().isoformat()
        append_jsonl_file(Config.CONTACTS_FILE, contact_data)
        return contact_data
    
    @staticmethod
    def delete_by_index(index):
        """根据索引删除联系记录"""
        contacts = ContactModel.load_contacts()
        if index < 0 or index >= len(contacts):
            return None
        
        deleted_contact = contacts.pop(index)
        save_jsonl_file(Config.CONTACTS_FILE, contacts)
        return deleted_contact
    
    @staticmethod
    def get_stats():
        """获取联系表单统计信息"""
        contacts = ContactModel.load_contacts()
        total = len(contacts)
        
        # 月度统计
        monthly_stats = {}
        for contact in contacts:
            timestamp = contact.get('timestamp', '')
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp)
                    month_key = date.strftime('%Y-%m')
                    monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
                except:
                    continue
        
        # 本月数量
        current_month = datetime.now().replace(day=1).isoformat()
        recent_count = len([c for c in contacts if c.get('timestamp', '') > current_month])
        
        return {
            "total": total,
            "monthly_stats": monthly_stats,
            "recent_count": recent_count
        }
