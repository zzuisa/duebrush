from flask import Flask
from flask_cors import CORS

from config import Config
from models.painting import PaintingModel
from models.contact import ContactModel
from models.site import SiteModel

from routes.auth import auth_bp
from routes.paintings import paintings_bp
from routes.contacts import contacts_bp
from routes.uploads import uploads_bp
from routes.site import site_bp
from routes.static import static_bp

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 配置CORS
    CORS(app)
    
    # 初始化配置
    Config.init_dirs()
    
    # 初始化数据文件
    PaintingModel.init_file()
    SiteModel.init_file()
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(paintings_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(site_bp)
    app.register_blueprint(static_bp)
    
    return app
