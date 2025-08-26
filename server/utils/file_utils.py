import os
import secrets
import json
from pathlib import Path
from config import Config

def slugify(value: str) -> str:
    """将字符串转换为URL友好的格式"""
    keep = []
    for ch in value.strip():
        if ch.isalnum():
            keep.append(ch.lower())
        elif ch in [' ', '-', '_']:
            keep.append('-')
    slug = ''.join(keep).strip('-')
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug or secrets.token_hex(4)

def generate_unique_filename(original_name, desired_name=None):
    """生成唯一的文件名"""
    original_name = original_name.replace('\\', '/').split('/')[-1]
    base_name, ext = os.path.splitext(original_name)
    
    if desired_name:
        safe_stem = slugify(desired_name)
    else:
        safe_stem = slugify(base_name) if base_name else secrets.token_hex(8)
    
    ext = (ext or '').lower() or '.jpg'
    
    # 确保唯一性，如果文件存在则添加后缀
    candidate = f"{safe_stem}{ext}"
    idx = 1
    while (Config.UPLOADS_DIR / candidate).exists():
        candidate = f"{safe_stem}-{idx}{ext}"
        idx += 1
    
    return candidate

def load_json_file(file_path):
    """加载JSON文件"""
    try:
        if file_path.exists():
            return json.loads(file_path.read_text(encoding='utf-8'))
        return {}
    except Exception:
        return {}

def save_json_file(file_path, data):
    """保存JSON文件"""
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def load_jsonl_file(file_path):
    """加载JSONL文件"""
    data = []
    if file_path.exists():
        with file_path.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data.append(json.loads(line))
                    except:
                        continue
    return data

def save_jsonl_file(file_path, data):
    """保存JSONL文件"""
    with file_path.open('w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def append_jsonl_file(file_path, item):
    """向JSONL文件追加数据"""
    with file_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
