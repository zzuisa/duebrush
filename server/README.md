# DueBrush 后端项目

## 项目概述

DueBrush 是一个基于 Flask 的 Web 应用后端，提供绘画作品展示、联系表单、文件上传等功能。

## 项目结构

```
server/
├── app/                    # 应用核心
│   ├── __init__.py
│   └── app.py             # Flask应用工厂
├── config.py              # 配置管理
├── models/                # 数据模型层
│   ├── __init__.py
│   ├── painting.py        # 绘画数据模型
│   ├── contact.py         # 联系表单数据模型
│   └── site.py            # 网站数据模型
├── routes/                # 路由层
│   ├── __init__.py
│   ├── auth.py            # 认证路由
│   ├── paintings.py       # 绘画管理路由
│   ├── contacts.py        # 联系表单路由
│   ├── uploads.py         # 文件上传路由
│   ├── site.py            # 网站数据路由
│   └── static.py          # 静态文件路由
├── utils/                 # 工具函数层
│   ├── __init__.py
│   ├── auth.py            # 认证工具
│   ├── email.py           # 邮件发送工具
│   └── file_utils.py      # 文件处理工具
├── tests/                 # 测试文件
│   ├── __init__.py
│   ├── test_app.py        # 应用测试
│   └── test_email.py      # 邮件测试
├── scripts/               # 脚本文件
│   ├── __init__.py
│   └── migrate.py         # 迁移脚本
├── docs/                  # 文档
│   ├── __init__.py
│   ├── README.md          # 项目文档
│   ├── EMAIL_SETUP.md     # 邮件配置指南
│   └── ARCHITECTURE.md    # 架构说明
├── data/                  # 数据文件
│   ├── paintings.json     # 绘画数据
│   ├── contacts.jsonl     # 联系表单数据
│   └── site.json          # 网站数据
├── uploads/               # 上传文件目录
├── .env                   # 环境变量配置
├── requirements.txt       # 依赖包列表
└── run.py                 # 应用启动文件
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并配置：

```env
# 管理员密码
ADMIN_PASSWORD=your-admin-password

# 邮件服务器配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com
```

### 3. 运行应用

```bash
python run.py
```

### 4. 测试功能

```bash
# 测试应用功能
python tests/test_app.py

# 测试邮件功能
python tests/test_email.py
```

## 主要功能

### 1. 绘画管理
- 获取绘画列表: `GET /api/paintings`
- 创建绘画: `POST /api/paintings`
- 更新绘画: `PUT /api/paintings/<id>`
- 删除绘画: `DELETE /api/paintings/<id>`

### 2. 联系表单
- 提交联系表单: `POST /api/contact`
- 获取联系记录: `GET /api/contacts`
- 获取统计信息: `GET /api/contacts/stats`

### 3. 文件上传
- 上传文件: `POST /api/upload`
- 访问文件: `GET /uploads/<filename>`

### 4. 网站数据
- 轮播图管理: `GET/POST /api/slider`
- 作者信息管理: `GET/POST /api/authors`

### 5. 认证
- 管理员登录: `POST /api/login`
- 健康检查: `GET /api/health`

## 开发指南

### 添加新功能

1. **创建数据模型** (在 `models/` 目录)
2. **添加路由处理** (在 `routes/` 目录)
3. **注册蓝图** (在 `app/app.py` 中)
4. **编写测试** (在 `tests/` 目录)

### 代码规范

- 使用 Python 3.8+
- 遵循 PEP 8 代码风格
- 添加适当的文档字符串
- 编写单元测试

## 部署

### 开发环境

```bash
python run.py
```

### 生产环境

推荐使用 Gunicorn 或 uWSGI：

```bash
# 使用 Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app.app:create_app()"

# 使用 uWSGI
uwsgi --http 0.0.0.0:5000 --module app.app:create_app
```

## 故障排除

### 常见问题

1. **邮件发送失败**
   - 检查 `.env` 文件配置
   - 确认邮箱应用专用密码正确
   - 运行 `python tests/test_email.py` 进行测试

2. **模块导入错误**
   - 确认所有依赖已安装
   - 检查 Python 路径设置
   - 运行 `python tests/test_app.py` 进行测试

3. **文件权限问题**
   - 确认 `data/` 和 `uploads/` 目录可写
   - 检查文件所有者权限

## 文档

- [项目文档](docs/README.md)
- [邮件配置指南](docs/EMAIL_SETUP.md)
- [架构说明](docs/ARCHITECTURE.md)

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。
