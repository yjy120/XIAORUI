# XIAORUI 智能教育平台

> 基于大模型与知识图谱的自适应学习平台 · FastAPI + Vue3

## 项目简介

XIAORUI 是一个面向 K12 场景的智能教育平台，将豆包大模型与知识图谱结合，围绕「诊断 → 学习 → 测评 → 巩固」闭环，为学生提供个性化学习路径，为教师提供课程与作业管理能力，为管理员提供全局运维视图。

## 核心功能

- **AI 学情诊断**：按学科或知识点自动生成诊断题，答题后由大模型分析错题、提取薄弱知识点并落库。
- **知识图谱**：以知识点（Node）与关联边（Edge）组织课程体系，支撑自适应推荐。
- **课程与作业**：教师创建课程、知识点、资源、题目与作业；学生按作业作答。
- **在线测评**：支持选择/主观题，自动判分与人工复核标记，记录学习时长与掌握度。
- **学习论坛**：发帖、回复、点赞、禁言等社区能力，配套消息通知。
- **三角色体系**：学生（student）/ 教师（teacher）/ 管理员（admin）分权访问。

## 技术栈

**后端**
- Python / FastAPI / Uvicorn
- SQLAlchemy + SQLite（轻量本地库，开箱即用）
- Pydantic 数据校验
- JWT（python-jose）+ passlib[bcrypt] 密码加密
- 豆包大模型（火山方舟 Ark API）驱动 AI 出题与错题分析

**前端**
- Vue 3 + Vite
- Element Plus + ECharts + Pinia + Vue Router + Axios + jwt-decode

## 目录结构

```
XIAORUI/
├── backend/
│   ├── app/
│   │   ├── main.py                 # 应用入口、路由注册、静态资源挂载
│   │   ├── models.py               # ORM 模型与建库初始化
│   │   ├── routers/                # auth / student / teacher / admin / quiz / forum / ai_engine
│   │   └── services/doubao_ai.py   # 大模型调用封装（含重试与 JSON 容错）
│   └── requirements.txt
└── frontend/                       # Vue 3 前端工程
```

## 快速开始

### 1. 配置大模型密钥

`backend/app/services/doubao_ai.py` 中的 API Key 已替换为占位符 `YOUR_DOUBAO_API_KEY`，请填入你自己的火山方舟密钥，或改为从环境变量读取后再运行。未配置时 AI 出题接口会走内置的降级题目兜底。

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- 服务地址：`http://localhost:8000`
- 接口文档（Swagger）：`http://localhost:8000/docs`
- 数据库：首次启动自动在本地创建 `xiaorui_full_system.db`

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

> 前端需 Node.js 20.19+ 或 22.12+。

## 说明

本项目为课程实践作品，大模型密钥、数据库等敏感配置均已从代码中移除，请以占位符或环境变量方式注入后再运行。
