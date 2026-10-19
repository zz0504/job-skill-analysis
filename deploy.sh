#!/bin/bash

echo "========================================="
echo "开始部署项目到服务器"
echo "========================================="

echo "1. 拉取最新代码..."
git pull origin master

echo "2. 安装后端依赖..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
else
    python3 -m venv venv
    source venv/bin/activate
fi
pip install -r requirements.txt

echo "3. 安装前端依赖并构建..."
cd ../frontend
npm install
npm run build

echo "4. 重启后端服务..."
cd ../backend

# 查找并停止旧的uvicorn进程
pkill -f uvicorn || true
sleep 2

# 启动新的服务
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > logs/app.log 2>&1 &

echo "5. 等待服务启动..."
sleep 3

echo "========================================="
echo "部署完成！"
echo "========================================="
echo "访问: http://YOUR_SERVER_IP"
echo "测试账号: test / 123456"
echo "========================================="
