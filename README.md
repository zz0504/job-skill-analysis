# 招聘岗位技能关键词分析系统

> 面向招聘数据的技能关键词分析平台：上传招聘岗位数据 → 自动清洗 → 中文分词提取技能关键词 → 生成词云、趋势与岗位技能矩阵 → 输出分析报告。

本科毕业设计项目。后端 FastAPI + MySQL，前端 Vue 3 + ECharts，含完整的 Linux 生产部署方案（Nginx 反向代理 + systemd 守护 + 一键部署脚本）。

---

## 功能

| 模块 | 说明 |
| --- | --- |
| 用户认证 | 注册 / 登录，JWT 签发与校验，bcrypt 密码哈希 |
| 数据上传 | 支持 CSV / Excel（.csv / .xlsx / .xls），单文件上限 50 MB |
| 数据清洗 | 去重、空值处理、字段标准化，异步执行并轮询进度 |
| 关键词分析 | 基于 **jieba** 中文分词 + 停用词过滤，统计技能词频与趋势 |
| 岗位技能矩阵 | 按岗位 × 技能构建矩阵，输出交叉表 |
| 可视化 | 词云、柱状图、趋势图（ECharts + echarts-wordcloud） |
| 分析报告 | 汇总生成可导出的分析结果 |

## 技术栈

**后端**：Python 3 · FastAPI · Uvicorn · SQLAlchemy 2.0 · PyMySQL · Pandas / NumPy · jieba · python-jose(JWT) · Passlib(bcrypt) · Redis（可选缓存）

**前端**：Vue 3 · Vite 5 · Vue Router · Pinia · Element Plus · ECharts · Tailwind CSS · Axios

**部署**：Linux (Ubuntu) · Nginx · systemd · MySQL 8 · uvicorn 多 worker

## 项目结构

```
job-skill-analysis/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # 路由：auth / upload / clean / keywords / matrix / report / batch
│   │   ├── core/          # 配置、数据库连接、JWT 鉴权、日志
│   │   ├── models/        # SQLAlchemy 模型（job / user）
│   │   ├── schemas/       # Pydantic 数据校验
│   │   ├── services/      # 业务逻辑：清洗、分词、矩阵、报告、缓存
│   │   ├── utils/         # CSV 解析、异常处理、示例数据生成
│   │   └── main.py
│   ├── requirements.txt
│   ├── init_db.sql / init_test_data.sql
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── views/         # LoginView / DataView / AnalysisView / ChartsView / ReportView
│   │   ├── api/           # Axios 封装与接口
│   │   └── stores/        # Pinia 状态
│   └── package.json
├── deploy/                # 生产部署
│   ├── nginx.conf         # 反向代理 + 静态资源缓存
│   ├── job-backend.service# systemd 单元，失败自动重启
│   ├── init.sh / deploy.sh# 环境初始化与一键部署
│   └── .env.production
└── 招聘岗位技能数据集_500条.xlsx   # 示例数据集
```

## 本地运行

### 1. 后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # 填入自己的 MySQL 账号密码

# 初始化数据库
mysql -u root -p < init_db.sql

# 创建默认账号（密码通过环境变量注入，见下）
python create_default_users.py

uvicorn app.main:app --reload --port 8000
```

接口文档：<http://localhost:8000/docs>

### 2. 前端

```bash
cd frontend
npm install
npm run dev                      # 默认 http://localhost:5173
npm run build                    # 产出 dist/
```

## 生产部署

项目已部署至 Linux 服务器，`deploy/` 目录提供完整方案：

```bash
cd deploy
chmod +x init.sh deploy.sh
sudo bash init.sh                # 安装 Nginx / MySQL / Python 依赖
sudo bash deploy.sh              # 构建前端、拉起后端、重载 Nginx
```

关键配置：

- **Nginx**：80 端口提供 `frontend/dist` 静态文件，`/api` 反向代理到 `127.0.0.1:8000`，静态资源 1 年缓存
- **systemd**：`Restart=on-failure` + `RestartSec=5`，2 个 uvicorn worker，日志接入 `journalctl`
- **配置与代码分离**：数据库密码、JWT 密钥全部走 `.env`，不进版本库

常用运维命令：

```bash
systemctl status job-backend
journalctl -u job-backend -f
tail -f /var/log/nginx/job-analysis.error.log
nginx -t && systemctl reload nginx
```

## 安全说明

仓库中**不包含任何真实凭据**。所有敏感配置以占位符形式出现：

- `backend/.env`、`deploy/.env.production` 未纳入版本控制，请从 `.env.example` 复制后自行填写
- `SECRET_KEY` 需替换为随机字符串：`python -c "import secrets;print(secrets.token_urlsafe(32))"`
- 默认账号密码通过环境变量 `DEFAULT_ADMIN_PASSWORD` / `DEFAULT_TEST_PASSWORD` 注入，未硬编码

## 待改进

- [ ] 接入 Redis 缓存（代码已就绪，开关在配置中）
- [ ] Dockerfile + docker-compose 一键启动
- [ ] GitHub Actions CI：自动跑测试与构建
- [ ] 关键词抽取增加自定义词典与同义词归并
