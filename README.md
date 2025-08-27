# Düsselbrush - 艺术家作品集网站

一个现代化的艺术家作品集网站，具有完整的前后端功能。

## 功能特性

### 前端功能
- 🎨 响应式设计，支持移动端
- 🖼️ 作品展示画廊
- 👤 作者信息展示
- 📧 联系表单（已优化）
- 🎠 轮播图展示
- 📱 移动端友好

### 后端功能
- 🔐 管理员认证系统
- 🖼️ 作品管理（CRUD）
- 👤 作者信息管理
- 📧 联系表单处理
- 📊 联系表单统计
- 📧 邮件通知功能
- 📁 文件上传管理

### 联系表单优化
- ✅ 实时表单验证
- ✅ 加载状态显示
- ✅ 错误提示优化
- ✅ 成功反馈
- ✅ 邮件通知
- ✅ 管理后台查看

## 技术栈

### 前端
- HTML5 + CSS3
- JavaScript (jQuery)
- Bootstrap 2.3.2
- 响应式设计

### 后端
- Python 3.x
- Flask 3.0.3
- Flask-CORS 4.0.0

## 安装和运行

### 1. 克隆项目
```bash
git clone <repository-url>
cd duebrush
```

### 2. 安装Python依赖
```bash
cd server
pip install -r requirements.txt
```

### 3. 配置环境变量（可选）
复制 `env.example` 为 `.env` 并配置：
```bash
cp env.example .env
```

编辑 `.env` 文件，配置邮件服务器：
```env
ADMIN_PASSWORD=your-admin-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@example.com
```

### 4. 运行开发服务器
```bash
# 方法1：使用Python直接运行
python app.py

# 方法2：使用开发服务器脚本
cd ..
python dev_server.py
```

### 5. 访问网站
- 前台：http://localhost:5000
- 管理后台：http://localhost:5000/admin
- 登录：http://localhost:5000/admin/login

## 管理后台使用

### 登录
- 默认密码：`brush2025`
- 可在环境变量中修改 `ADMIN_PASSWORD`

### 功能模块
1. **画作管理** - 添加、编辑、删除作品
2. **轮播图管理** - 管理首页轮播图
3. **作者信息管理** - 管理作者资料
4. **联系表单管理** - 查看和管理联系表单

## 联系表单功能

### 用户端
- 实时表单验证
- 友好的错误提示
- 加载状态显示
- 成功反馈

### 管理端
- 查看所有联系记录
- 统计信息显示
- 详情查看
- 删除记录

### 邮件通知
配置邮件服务器后，新联系表单会自动发送通知邮件给管理员。

## 文件结构

```
duebrush/
├── _include/           # 静态资源
│   ├── css/           # 样式文件
│   ├── js/            # JavaScript文件
│   └── img/           # 图片资源
├── admin/             # 管理后台
├── server/            # 后端代码
│   ├── app.py         # Flask应用
│   ├── data/          # 数据文件
│   └── uploads/       # 上传文件
├── index.html         # 主页
└── dev_server.py      # 开发服务器
```

## API接口

### 认证
- `POST /api/login` - 管理员登录

### 作品管理
- `GET /api/paintings` - 获取作品列表
- `POST /api/paintings` - 创建作品
- `GET /api/paintings/<id>` - 获取作品详情
- `PUT /api/paintings/<id>` - 更新作品
- `DELETE /api/paintings/<id>` - 删除作品

### 联系表单
- `POST /api/contact` - 提交联系表单
- `GET /api/contacts` - 获取联系记录（需认证）
- `GET /api/contacts/stats` - 获取统计信息（需认证）
- `DELETE /api/contacts/<id>` - 删除记录（需认证）

### 作者管理
- `GET /api/authors` - 获取作者列表
- `POST /api/authors` - 创建作者（需认证）
- `PUT /api/authors/<id>` - 更新作者（需认证）
- `DELETE /api/authors/<id>` - 删除作者（需认证）

### 轮播图管理
- `GET /api/slider` - 获取轮播图
- `POST /api/slider` - 更新轮播图（需认证）

## 部署

### 生产环境部署
1. 配置生产环境变量
2. 使用 Gunicorn 或 uWSGI 部署
3. 配置 Nginx 反向代理
4. 设置 SSL 证书

### Docker 部署（可选）
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY server/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "server/app.py"]
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License


