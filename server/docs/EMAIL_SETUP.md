# 邮件配置指南

## 概述

本指南将帮助您配置邮件发送功能，解决邮件发送问题。

## 环境变量配置

在运行应用之前，请设置以下环境变量：

### Windows PowerShell
```powershell
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "465"  # 或 "587"
$env:SMTP_USERNAME = "your-email@gmail.com"
$env:SMTP_PASSWORD = "your-app-password"
$env:ADMIN_EMAIL = "admin@example.com"
```

### Windows CMD
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=465
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set ADMIN_EMAIL=admin@example.com
```

### Linux/Mac
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=465
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
export ADMIN_EMAIL=admin@example.com
```

### 使用 .env 文件（推荐）
在 `server` 目录下创建 `.env` 文件：
```env
# 管理员密码
ADMIN_PASSWORD=brush2025

# 邮件服务器配置
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com
```

## 端口配置说明

### 端口 465 (SSL)
- 使用 SSL 加密连接
- 更安全，推荐使用
- 配置示例：
  ```
  SMTP_PORT=465
  ```

### 端口 587 (TLS)
- 使用 STARTTLS 加密连接
- 兼容性更好
- 配置示例：
  ```
  SMTP_PORT=587
  ```

## Gmail 配置说明

### 1. 启用两步验证
1. 登录您的 Gmail 账户
2. 进入"安全性"设置
3. 启用"两步验证"

### 2. 生成应用专用密码
1. 在"安全性"设置中找到"应用专用密码"
2. 选择"邮件"应用
3. 生成16位应用专用密码
4. 使用此密码作为 `SMTP_PASSWORD`

### 3. 允许不太安全的应用访问（不推荐）
- 如果不想使用应用专用密码，可以在 Gmail 设置中允许不太安全的应用访问
- 但这种方式安全性较低，不推荐使用

## 其他邮箱服务配置

### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### QQ邮箱
```
SMTP_SERVER=smtp.qq.com
SMTP_PORT=465
```

### 163邮箱
```
SMTP_SERVER=smtp.163.com
SMTP_PORT=465
```

## 调试步骤

### 1. 测试环境变量加载
```bash
cd server
python tests/test_email.py
```

### 2. 运行调试脚本
```bash
cd server
python tests/test_email.py
```

### 3. 检查控制台输出
调试脚本会显示详细的配置信息和错误信息。

### 4. 常见问题排查

#### 问题1: 认证失败
```
[DEBUG] ❌ SMTP认证失败
```
**解决方案:**
- 检查邮箱和密码是否正确
- 确认使用的是应用专用密码而不是登录密码
- 确认两步验证已启用

#### 问题2: 连接失败
```
[DEBUG] ❌ SMTP连接错误
```
**解决方案:**
- 检查SMTP服务器地址和端口是否正确
- 检查网络连接
- 确认防火墙设置

#### 问题3: 发件人拒绝
```
[DEBUG] ❌ 发件人拒绝
```
**解决方案:**
- 确认发件人邮箱地址正确
- 检查邮箱服务商的发送限制

#### 问题4: 收件人拒绝
```
[DEBUG] ❌ 收件人拒绝
```
**解决方案:**
- 确认收件人邮箱地址正确
- 检查收件人邮箱是否已满或设置了过滤规则

## 测试邮件发送

### 1. 使用调试脚本
```bash
python tests/test_email.py
```

### 2. 使用API测试
启动应用后，发送POST请求到：
```
POST /api/test-email
```

### 3. 测试联系表单
提交联系表单后，检查控制台输出的调试信息。

## 日志查看

### 1. 应用日志
启动应用时，所有调试信息会显示在控制台中。

### 2. 邮件发送日志
每次邮件发送都会显示详细的步骤信息：
- 配置信息
- 连接状态
- 认证结果
- 发送结果

## 安全注意事项

1. **不要将密码硬编码在代码中**
2. **使用环境变量管理敏感信息**
3. **定期更换应用专用密码**
4. **监控邮件发送日志**
5. **设置合理的发送频率限制**

## 故障排除

### 如果邮件仍然无法发送：

1. **检查环境变量**
   ```bash
   echo $SMTP_USERNAME
   echo $SMTP_PASSWORD
   ```

2. **测试网络连接**
   ```bash
   telnet smtp.gmail.com 465
   ```

3. **检查邮箱设置**
   - 确认邮箱服务商允许SMTP访问
   - 检查是否有发送限制

4. **查看详细错误信息**
   - 运行调试脚本获取详细错误信息
   - 根据错误信息进行针对性排查

## 联系支持

如果按照以上步骤仍然无法解决问题，请提供以下信息：
1. 调试脚本的完整输出
2. 使用的邮箱服务商
3. 错误信息截图
4. 环境变量配置（隐藏密码）
