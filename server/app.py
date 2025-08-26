from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import secrets
from functools import wraps
from pathlib import Path


def create_app():
    app = Flask(__name__)
    CORS(app)

    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    paintings_file = data_dir / 'paintings.json'
    contacts_file = data_dir / 'contacts.jsonl'
    uploads_dir = Path(__file__).parent / 'uploads'
    uploads_dir.mkdir(parents=True, exist_ok=True)
    site_file = data_dir / 'site.json'

    # Simple auth setup
    admin_password = os.getenv('ADMIN_PASSWORD', 'brush2025')
    active_tokens = set()

    def require_auth(f):
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

    if not paintings_file.exists():
        paintings_file.write_text(json.dumps({"paintings": []}, ensure_ascii=False, indent=2), encoding='utf-8')
    if not site_file.exists():
        site_file.write_text(json.dumps({"slider": [], "authors": []}, ensure_ascii=False, indent=2), encoding='utf-8')

    @app.get('/api/health')
    def health():
        return jsonify({"status": "ok"})

    @app.post('/api/login')
    def login():
        payload = request.get_json(silent=True) or {}
        password = payload.get('password')
        if not password:
            return jsonify({"success": False, "message": "Password required"}), 400
        if password != admin_password:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
        token = secrets.token_urlsafe(24)
        active_tokens.add(token)
        return jsonify({"success": True, "token": token})

    # Paintings CRUD
    def load_paintings():
        try:
            return json.loads(paintings_file.read_text(encoding='utf-8'))
        except Exception:
            return {"paintings": []}

    def save_paintings(data):
        paintings_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    @app.get('/api/paintings')
    def list_paintings():
        data = load_paintings()
        return jsonify(data["paintings"])

    @app.post('/api/paintings')
    @require_auth
    def create_painting():
        payload = request.get_json(silent=True) or {}
        data = load_paintings()
        existing_ids = {p.get('id') for p in data['paintings']}
        next_id = (max(existing_ids) + 1) if existing_ids and all(isinstance(x, int) for x in existing_ids) else 1
        payload['id'] = payload.get('id', next_id)
        data['paintings'].append(payload)
        save_paintings(data)
        return jsonify(payload), 201

    @app.get('/api/paintings/<int:pid>')
    def get_painting(pid):
        data = load_paintings()
        for p in data['paintings']:
            if p.get('id') == pid:
                return jsonify(p)
        return jsonify({"error": "Not Found"}), 404

    @app.put('/api/paintings/<int:pid>')
    @app.patch('/api/paintings/<int:pid>')
    @require_auth
    def update_painting(pid):
        payload = request.get_json(silent=True) or {}
        data = load_paintings()
        for idx, p in enumerate(data['paintings']):
            if p.get('id') == pid:
                data['paintings'][idx] = {**p, **payload, 'id': pid}
                save_paintings(data)
                return jsonify(data['paintings'][idx])
        return jsonify({"error": "Not Found"}), 404

    @app.delete('/api/paintings/<int:pid>')
    @require_auth
    def delete_painting(pid):
        data = load_paintings()
        new_list = [p for p in data['paintings'] if p.get('id') != pid]
        if len(new_list) == len(data['paintings']):
            return jsonify({"error": "Not Found"}), 404
        data['paintings'] = new_list
        save_paintings(data)
        return jsonify({"status": "deleted", "id": pid})

    # Contact API
    @app.post('/api/contact')
    def contact():
        payload = request.get_json(silent=True) or request.form.to_dict()
        if not payload.get('email') or not payload.get('message'):
            return jsonify({"success": False, "message": "Email and message are required"}), 400
        line = json.dumps({**payload}, ensure_ascii=False)
        with contacts_file.open('a', encoding='utf-8') as f:
            f.write(line + "\n")
        return jsonify({"success": True})

    # Uploads
    @app.post('/api/upload')
    @require_auth
    def upload_file():
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "Empty filename"}), 400
        # Determine target filename
        raw_client_name = request.form.get('filename', '').strip()
        original_name = file.filename.replace('\\', '/').split('/')[-1]
        base_name, ext = os.path.splitext(original_name)

        def slugify(value: str) -> str:
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

        if raw_client_name:
            desired = slugify(raw_client_name)
            safe_stem = desired
        else:
            safe_stem = slugify(base_name) if base_name else secrets.token_hex(8)

        ext = (ext or '').lower() or '.jpg'

        # Ensure uniqueness by suffixing -1, -2, ... if exists
        candidate = f"{safe_stem}{ext}"
        idx = 1
        while (uploads_dir / candidate).exists():
            candidate = f"{safe_stem}-{idx}{ext}"
            idx += 1

        save_path = uploads_dir / candidate
        file.save(str(save_path))
        url_path = f"/uploads/{candidate}"
        return jsonify({"success": True, "url": url_path, "path": url_path, "filename": candidate})

    @app.get('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(str(uploads_dir), filename)

    # 开发环境静态文件服务
    @app.get('/')
    def serve_index():
        return send_from_directory(str(Path(__file__).parent.parent), 'index.html')

    @app.get('/admin/')
    @app.get('/admin')
    def serve_admin():
        return send_from_directory(str(Path(__file__).parent.parent / 'admin'), 'index.html')

    @app.get('/admin/login')
    def serve_admin_login():
        return send_from_directory(str(Path(__file__).parent.parent / 'admin'), 'login.html')

    @app.get('/<path:filename>')
    def serve_static(filename):
        # 服务静态文件
        static_paths = [
            Path(__file__).parent.parent / '_include',
            Path(__file__).parent.parent
        ]
        
        for static_path in static_paths:
            file_path = static_path / filename
            if file_path.exists() and file_path.is_file():
                return send_from_directory(str(static_path), filename)
        
        # 如果文件不存在，返回404
        return jsonify({"error": "Not Found"}), 404

    # Site data: slider and author
    def load_site():
        try:
            return json.loads(site_file.read_text(encoding='utf-8'))
        except Exception:
            return {"slider": [], "authors": []}

    def save_site(data):
        site_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    @app.get('/api/slider')
    def get_slider():
        data = load_site()
        return jsonify(data.get('slider', []))

    @app.post('/api/slider')
    @require_auth
    def set_slider():
        payload = request.get_json(silent=True) or []
        if not isinstance(payload, list):
            return jsonify({"success": False, "message": "Expect list"}), 400
        data = load_site()
        data['slider'] = payload
        save_site(data)
        return jsonify({"success": True})

    @app.get('/api/authors')
    def get_authors():
        data = load_site()
        return jsonify(data.get('authors', []))

    @app.post('/api/authors')
    @require_auth
    def create_author():
        payload = request.get_json(silent=True) or {}
        data = load_site()
        authors = data.get('authors', [])
        existing_ids = {a.get('id') for a in authors}
        next_id = (max(existing_ids) + 1) if existing_ids and all(isinstance(x, int) for x in existing_ids) else 1
        new_author = {
            'id': next_id,
            'name': payload.get('name', ''),
            'position': payload.get('position', ''),
            'bio': payload.get('bio', ''),
            'avatar': payload.get('avatar', ''),
            'social': payload.get('social', {})
        }
        authors.append(new_author)
        data['authors'] = authors
        save_site(data)
        return jsonify(new_author), 201

    @app.get('/api/authors/<int:aid>')
    def get_author(aid):
        data = load_site()
        authors = data.get('authors', [])
        for author in authors:
            if author.get('id') == aid:
                return jsonify(author)
        return jsonify({"error": "Not Found"}), 404

    @app.put('/api/authors/<int:aid>')
    @app.patch('/api/authors/<int:aid>')
    @require_auth
    def update_author(aid):
        payload = request.get_json(silent=True) or {}
        data = load_site()
        authors = data.get('authors', [])
        for idx, author in enumerate(authors):
            if author.get('id') == aid:
                authors[idx] = {**author, **payload, 'id': aid}
                save_site(data)
                return jsonify(authors[idx])
        return jsonify({"error": "Not Found"}), 404

    @app.delete('/api/authors/<int:aid>')
    @require_auth
    def delete_author(aid):
        data = load_site()
        authors = data.get('authors', [])
        new_list = [a for a in authors if a.get('id') != aid]
        if len(new_list) == len(authors):
            return jsonify({"error": "Not Found"}), 404
        data['authors'] = new_list
        save_site(data)
        return jsonify({"status": "deleted", "id": aid})

    # 保持向后兼容的单个作者API
    @app.get('/api/author')
    def get_author_legacy():
        data = load_site()
        authors = data.get('authors', [])
        if authors:
            return jsonify(authors[0])
        return jsonify({"name": "", "bio": "", "avatar": ""})

    @app.post('/api/author')
    @require_auth
    def set_author_legacy():
        payload = request.get_json(silent=True) or {}
        data = load_site()
        authors = data.get('authors', [])
        if authors:
            # 更新第一个作者
            authors[0].update({
                'name': payload.get('name', authors[0].get('name', '')),
                'bio': payload.get('bio', authors[0].get('bio', '')),
                'avatar': payload.get('avatar', authors[0].get('avatar', '')),
            })
        else:
            # 创建第一个作者
            authors.append({
                'id': 1,
                'name': payload.get('name', ''),
                'position': '',
                'bio': payload.get('bio', ''),
                'avatar': payload.get('avatar', ''),
                'social': {}
            })
        data['authors'] = authors
        save_site(data)
        return jsonify({"success": True, "author": authors[0]})

    return app


if __name__ == '__main__':
    app = create_app()
    # Flask 3.0.3 + Werkzeug 3 支持 reloader_type='stat'，避免监听非代码文件（如 uploads）
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)




