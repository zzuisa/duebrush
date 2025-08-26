#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
应用功能测试
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试所有模块的导入"""
    try:
        print("测试配置模块...")
        from config import Config
        print("✓ 配置模块导入成功")
        
        print("测试工具函数模块...")
        from utils.auth import require_auth, generate_token
        from utils.email import validate_email, send_notification_email
        from utils.file_utils import slugify, generate_unique_filename
        print("✓ 工具函数模块导入成功")
        
        print("测试数据模型模块...")
        from models.painting import PaintingModel
        from models.contact import ContactModel
        from models.site import SiteModel
        print("✓ 数据模型模块导入成功")
        
        print("测试路由模块...")
        from routes.auth import auth_bp
        from routes.paintings import paintings_bp
        from routes.contacts import contacts_bp
        from routes.uploads import uploads_bp
        from routes.site import site_bp
        from routes.static import static_bp
        print("✓ 路由模块导入成功")
        
        print("测试主应用...")
        from app.app import create_app
        print("✓ 主应用导入成功")
        
        print("\n🎉 所有模块导入成功！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_app_creation():
    """测试应用创建"""
    try:
        from app.app import create_app
        app = create_app()
        print("✓ 应用创建成功")
        return True
    except Exception as e:
        print(f"❌ 应用创建失败: {e}")
        return False

def main():
    """主函数"""
    print("应用功能测试")
    print("=" * 50)
    
    # 测试导入
    import_success = test_imports()
    
    if import_success:
        print("\n测试应用创建...")
        app_success = test_app_creation()
        
        if app_success:
            print("\n✅ 应用测试全部通过！")
        else:
            print("\n❌ 应用创建测试失败")
    else:
        print("\n❌ 导入测试失败")

if __name__ == "__main__":
    main()
