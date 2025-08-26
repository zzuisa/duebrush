#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
迁移脚本：从旧版本迁移到重构后的版本
"""

import os
import shutil
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def backup_original():
    """备份原始文件"""
    try:
        if os.path.exists('app.py'):
            shutil.copy2('app.py', 'app_backup.py')
            print("✓ 已备份原始 app.py 为 app_backup.py")
            return True
        else:
            print("⚠ 未找到 app.py 文件")
            return False
    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return False

def check_dependencies():
    """检查依赖项"""
    required_files = [
        'app/app.py',
        'config.py',
        'models/__init__.py',
        'models/painting.py',
        'models/contact.py',
        'models/site.py',
        'routes/__init__.py',
        'routes/auth.py',
        'routes/paintings.py',
        'routes/contacts.py',
        'routes/uploads.py',
        'routes/site.py',
        'routes/static.py',
        'utils/__init__.py',
        'utils/auth.py',
        'utils/email.py',
        'utils/file_utils.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✓ 所有必需文件都存在")
    return True

def test_new_app():
    """测试新应用"""
    try:
        # 测试导入
        from app.app import create_app
        
        # 测试应用创建
        app = create_app()
        print("✓ 新应用创建成功")
        return True
    except Exception as e:
        print(f"❌ 新应用测试失败: {e}")
        return False

def migrate():
    """执行迁移"""
    print("开始迁移到重构版本...\n")
    
    # 1. 检查依赖
    print("1. 检查依赖项...")
    if not check_dependencies():
        print("❌ 依赖检查失败，请确保所有重构文件都已创建")
        return False
    
    # 2. 备份原始文件
    print("\n2. 备份原始文件...")
    if not backup_original():
        print("⚠ 备份失败，但继续迁移")
    
    # 3. 测试新应用
    print("\n3. 测试新应用...")
    if not test_new_app():
        print("❌ 新应用测试失败，迁移中止")
        return False
    
    print("\n✅ 迁移完成！新应用运行正常")
    print("💡 使用 'python run.py' 启动应用")
    return True

def rollback():
    """回滚到原始版本"""
    print("开始回滚...")
    
    try:
        if os.path.exists('app_backup.py'):
            shutil.move('app_backup.py', 'app.py')
            print("✓ 已回滚到原始版本")
            return True
        else:
            print("❌ 未找到备份文件")
            return False
    except Exception as e:
        print(f"❌ 回滚失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'rollback':
            rollback()
        elif command == 'test':
            test_new_app()
        else:
            print("用法: python scripts/migrate.py [rollback|test]")
    else:
        migrate()

if __name__ == "__main__":
    main()
