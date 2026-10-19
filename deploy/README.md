# 部署指南

## 🚀 快速部署流程

### 方法一：使用远程开发（推荐）

1. **连接到服务器**
   - 使用VS Code Remote SSH或其他远程开发工具连接服务器
   
2. **克隆或上传项目**
   ```bash
   # 如果使用git
   git clone <your-repo-url> /var/www/job-analysis
   
   # 或者直接上传项目文件到 /var/www/job-analysis
   ```

3. **运行部署脚本**
   ```bash
   cd /var/www/job-analysis/deploy
   chmod +x deploy.sh init.sh
   sudo bash init.sh
   sudo bash deploy.sh
   ```

### 方法二：手动上传部署

1. **准备服务器**
   ```bash
   # SSH连接服务器
   ssh root@你的服务器IP
   
   # 创建目录
   mkdir -p /var/www/job-analysis
   ```

2. **上传项目文件**
   - 使用SCP、SFTP或rsync上传整个项目到服务器
   ```bash
   # 本地执行
   scp -r D:/毕业设计项目/* root@服务器IP:/var/www/job-analysis/
   ```

3. **执行部署**
   ```bash
   cd /var/www/job-analysis/deploy
   chmod +x deploy.sh init.sh
   sudo bash init.sh
   sudo bash deploy.sh
   ```

---

## ⚙️ 配置说明

### 修改数据库密码（重要）

编辑 `deploy/.env.production` 文件：
```bash
MYSQL_PASSWORD=你的强密码
```

同时在 `deploy/deploy.sh` 中修改：
```bash
MYSQL_PASSWORD="你的强密码"
```

### 修改前端API地址

如果使用域名，需要修改前端配置：
```bash
# 编辑 frontend/src/api/index.js 或相关API配置文件
# 将 localhost 改为实际域名或IP
```

---

## 📋 部署后操作

### 检查服务状态
```bash
# 后端服务
systemctl status job-backend

# Nginx
systemctl status nginx

# MySQL
systemctl status mysql
```

### 查看日志
```bash
# 后端日志
journalctl -u job-backend -f

# Nginx访问日志
tail -f /var/log/nginx/job-analysis.access.log

# Nginx错误日志
tail -f /var/log/nginx/job-analysis.error.log
```

### 重启服务
```bash
# 重启后端
systemctl restart job-backend

# 重启Nginx
systemctl restart nginx

# 重启所有服务
systemctl restart job-backend nginx mysql
```

---

## 🔧 常见问题

### 1. 端口被占用
```bash
# 查看8000端口占用
lsof -i:8000
# 杀死进程
kill -9 <PID>
```

### 2. 数据库连接失败
```bash
# 检查MySQL状态
systemctl status mysql

# 测试连接
mysql -u jobuser -p
```

### 3. 权限问题
```bash
# 修复权限
chown -R www-data:www-data /var/www/job-analysis
chmod -R 755 /var/www/job-analysis
```

### 4. 前端空白页
```bash
# 检查构建
cd /var/www/job-analysis/frontend
npm run build

# 检查Nginx配置
nginx -t
```

---

## 🌐 HTTPS配置（可选）

使用Let's Encrypt配置HTTPS：
```bash
# 安装certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d 你的域名

# 自动续期
certbot renew --dry-run
```

---

## 🔄 更新部署

当代码更新后：
```bash
cd /var/www/job-analysis

# 拉取最新代码（如果使用git）
git pull

# 更新后端
cd backend
source .venv/bin/activate
pip install -r requirements.txt
systemctl restart job-backend

# 更新前端
cd ../frontend
npm install
npm run build

# 重启Nginx
systemctl restart nginx
```

---

## 📊 性能优化建议

1. **启用Gzip压缩**（已在Nginx配置中启用）
2. **配置CDN**（静态资源加速）
3. **数据库优化**（添加索引、配置连接池）
4. **Redis缓存**（已配置，可选启用）
5. **负载均衡**（高并发场景）

---

## 🔒 安全建议

1. 修改数据库默认密码
2. 配置防火墙只开放必要端口
3. 定期更新系统和依赖
4. 配置HTTPS
5. 设置文件上传大小限制
6. 定期备份数据库
