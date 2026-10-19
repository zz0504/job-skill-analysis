#!/bin/bash

# ============================================
# 一键部署脚本 - 招聘岗位技能关键词分析系统
# ============================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 默认配置
PROJECT_DIR="/var/www/job-analysis"
MYSQL_DATABASE="job_skill_analysis"
MYSQL_USER="jobuser"
MYSQL_PASSWORD="CHANGE_ME_DB_PASSWORD"
BACKEND_PORT=8000

# 检查是否为root用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用root用户运行此脚本"
        exit 1
    fi
}

# 安装系统依赖
install_dependencies() {
    log_step "安装系统依赖..."
    
    # 检测系统类型
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        apt update
        apt install -y python3.10 python3.10-venv python3-pip \
                       nodejs npm \
                       mysql-server \
                       nginx \
                       redis-server \
                       git curl wget
    elif [ -f /etc/redhat-release ]; then
        # CentOS/RHEL
        yum install -y python310 python310-pip \
                       nodejs npm \
                       mysql-server \
                       nginx \
                       redis \
                       git curl wget
    else
        log_error "不支持的系统类型"
        exit 1
    fi
    
    log_info "系统依赖安装完成"
}

# 配置MySQL
setup_mysql() {
    log_step "配置MySQL数据库..."
    
    # 启动MySQL
    systemctl start mysql || systemctl start mysqld
    systemctl enable mysql || systemctl enable mysqld
    
    # 创建数据库和用户
    mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF
    
    log_info "MySQL配置完成"
}

# 配置Redis
setup_redis() {
    log_step "配置Redis..."
    
    systemctl start redis-server || systemctl start redis
    systemctl enable redis-server || systemctl enable redis
    
    log_info "Redis配置完成"
}

# 部署后端
deploy_backend() {
    log_step "部署后端应用..."
    
    cd ${PROJECT_DIR}/backend
    
    # 创建虚拟环境
    if [ ! -d ".venv" ]; then
        python3.10 -m venv .venv
    fi
    
    # 激活虚拟环境并安装依赖
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 复制环境配置
    if [ -f "../deploy/.env.production" ]; then
        cp ../deploy/.env.production .env
    fi
    
    # 创建必要目录
    mkdir -p logs uploads
    chown -R www-data:www-data logs uploads
    
    # 导入数据库初始化脚本
    if [ -f "init_db.sql" ]; then
        mysql -u ${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DATABASE} < init_db.sql || true
    fi
    
    deactivate
    
    log_info "后端部署完成"
}

# 部署前端
deploy_frontend() {
    log_step "部署前端应用..."
    
    cd ${PROJECT_DIR}/frontend
    
    # 安装依赖
    npm install
    
    # 构建生产版本
    npm run build
    
    log_info "前端部署完成"
}

# 配置Nginx
setup_nginx() {
    log_step "配置Nginx..."
    
    # 复制配置文件
    cp ${PROJECT_DIR}/deploy/nginx.conf /etc/nginx/sites-available/job-analysis
    
    # 创建软链接
    if [ ! -L /etc/nginx/sites-enabled/job-analysis ]; then
        ln -s /etc/nginx/sites-available/job-analysis /etc/nginx/sites-enabled/
    fi
    
    # 删除默认配置
    rm -f /etc/nginx/sites-enabled/default
    
    # 测试并重启
    nginx -t
    systemctl restart nginx
    systemctl enable nginx
    
    log_info "Nginx配置完成"
}

# 配置systemd服务
setup_systemd() {
    log_step "配置后端服务..."
    
    # 复制服务文件
    cp ${PROJECT_DIR}/deploy/job-backend.service /etc/systemd/system/
    
    # 重载并启动
    systemctl daemon-reload
    systemctl enable job-backend
    systemctl start job-backend
    
    log_info "后端服务配置完成"
}

# 配置防火墙
setup_firewall() {
    log_step "配置防火墙..."
    
    if command -v ufw &> /dev/null; then
        ufw allow 22
        ufw allow 80
        ufw allow 443
        echo "y" | ufw enable
    elif command -v firewalld &> /dev/null; then
        firewall-cmd --permanent --add-port=22/tcp
        firewall-cmd --permanent --add-port=80/tcp
        firewall-cmd --permanent --add-port=443/tcp
        firewall-cmd --reload
    fi
    
    log_info "防火墙配置完成"
}

# 健康检查
health_check() {
    log_step "执行健康检查..."
    
    sleep 5
    
    # 检查后端
    if curl -s http://localhost:${BACKEND_PORT}/docs > /dev/null; then
        log_info "后端API正常运行"
    else
        log_warn "后端API可能未正常启动，请检查日志"
    fi
    
    # 检查前端
    if curl -s http://localhost > /dev/null; then
        log_info "前端服务正常运行"
    else
        log_warn "前端服务可能未正常启动"
    fi
    
    # 显示服务状态
    systemctl status job-backend --no-pager
    systemctl status nginx --no-pager
}

# 显示完成信息
show_complete() {
    echo ""
    echo "============================================"
    echo -e "${GREEN}部署完成！${NC}"
    echo "============================================"
    echo ""
    echo "访问地址:"
    echo "  前端: http://$(curl -s ifconfig.me || echo '服务器IP')"
    echo "  API文档: http://$(curl -s ifconfig.me || echo '服务器IP')/docs"
    echo ""
    echo "常用命令:"
    echo "  查看后端日志: journalctl -u job-backend -f"
    echo "  重启后端: systemctl restart job-backend"
    echo "  查看Nginx日志: tail -f /var/log/nginx/job-analysis.access.log"
    echo ""
    echo "数据库信息:"
    echo "  数据库: ${MYSQL_DATABASE}"
    echo "  用户: ${MYSQL_USER}"
    echo "  密码: ${MYSQL_PASSWORD}"
    echo "============================================"
}

# 主函数
main() {
    echo ""
    echo "============================================"
    echo "  招聘岗位技能关键词分析系统 - 一键部署"
    echo "============================================"
    echo ""
    
    check_root
    
    # 询问是否继续
    read -p "是否继续部署？(y/n): " confirm
    if [ "$confirm" != "y" ]; then
        echo "部署已取消"
        exit 0
    fi
    
    # 执行部署步骤
    install_dependencies
    setup_mysql
    setup_redis
    deploy_backend
    deploy_frontend
    setup_nginx
    setup_systemd
    setup_firewall
    health_check
    show_complete
}

# 运行
main "$@"
