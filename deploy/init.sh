#!/bin/bash

# ============================================
# 项目上传后初始化脚本
# ============================================

set -e

PROJECT_DIR="/var/www/job-analysis"

echo "创建项目目录..."
mkdir -p ${PROJECT_DIR}
mkdir -p ${PROJECT_DIR}/backend/logs
mkdir -p ${PROJECT_DIR}/backend/uploads

echo "设置目录权限..."
chown -R www-data:www-data ${PROJECT_DIR}
chmod -R 755 ${PROJECT_DIR}

echo "初始化完成！"
echo ""
echo "请将项目文件上传到: ${PROJECT_DIR}"
echo "然后运行: bash ${PROJECT_DIR}/deploy/deploy.sh"
