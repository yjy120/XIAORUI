# XIAORUI 智能教育平台

> 基于大模型与知识图谱的自适应学习平台 · FastAPI + Vue 3 + 豆包大模型

| FastAPI | Vue 3 | SQLAlchemy | 豆包大模型 | 知识图谱 | JWT |
|---|---|---|---|---|---|

## 一、项目概述

XIAORUI 是一个面向 K12 场景的智能教育平台，将**豆包大模型**与**知识图谱**结合，围绕「**AI 诊断 → 定位薄弱点 → 生成学习路径 → 课程学习 → 作业测评 → 巩固提升**」的闭环，为学生提供个性化学习路径，为教师提供课程、作业与学情分析能力，为管理员提供全局运维视图。

**项目规模**：14 张数据表、7 组业务路由、4 项 AI 能力、知识图谱可视化、三级角色权限体系。

## 二、核心功能

### 学生端

- **AI 学情诊断**：支持按学科（subject）或知识点（topic）两种模式，由大模型生成 5 道诊断题。
- **错题分析**：提交错题后由 AI 提取薄弱知识点，自动写入 `learning_records`，并记录掌握度。
- **学习路径推荐**：根据薄弱点由 AI 生成个性化学习步骤与推理说明。
- **课程学习**：查看已发布课程、课程资源，按知识点图谱进行结构化学习。
- **作业测评**：查看作业列表与完成状态（未开始/进行中/待批改/已完成），提交答案、查看得分与教师评语。
- **学习论坛**：发帖、回复、点赞，支持禁言管理；教师批改后自动写入消息通知。
- **个人中心**：学习时长、学习天数、答题数、能力雷达图数据。

### 教师端

- 课程创建与发布（draft / published 状态流转）
- 知识点与知识图谱边（先修关系）维护
- 作业创建、题目管理、主观题批改与评语
- 调用大模型生成**班级学情分析报告**（Markdown）

### 管理端

- 用户账号与角色管理、全局配置维护

## 三、技术架构

```
浏览器 (Vue 3 + Vite + Element Plus + Pinia + ECharts)
        │  REST API（JWT）
        ▼
FastAPI 后端
  ├─ routers/       # auth / student / teacher / admin / quiz / forum / ai_engine
  ├─ services/      # doubao_ai.py：大模型调用封装（重试 + JSON 容错 + 降级）
  ├─ models.py      # SQLAlchemy ORM，14 张表 + 关系映射
  └─ SQLite         # 本地轻量库，首次启动自动建库
         │  HTTPS
         ▼
豆包大模型（火山方舟 Ark API）
```

**技术选型**

- **后端**：Python、FastAPI、Uvicorn、SQLAlchemy、Pydantic、SQLite、JWT（python-jose）、passlib[bcrypt]、豆包大模型（doubao-seed）
- **前端**：Vue 3、Vite、Element Plus、Pinia、Vue Router、Axios、ECharts、jwt-decode
- **数据建模**：14 张表，含 `knowledge_nodes` / `knowledge_edges` 图谱表、`homeworks` 独立作业表

## 四、技术亮点

**1. 大模型服务封装：重试 + JSON 容错 + 三级降级**
`DoubaoService._call_ai()` 统一封装所有 AI 调用：自动去除 ````json` 代码块标记后解析、失败重试（默认 2 次）；上层业务对**每个 AI 能力**（出题 / 错题分析 / 学习路径 / 班级报告）都配置了专属兜底数据。即使大模型完全不可用，平台核心流程仍可运行——这是生产级 AI 应用的关键设计。

**2. 知识图谱驱动的自适应学习**
用 `KnowledgeNode`（知识点 + 权重）与 `KnowledgeEdge`（先修关系）建图；`/ai-engine/knowledge-graph/{course_id}` 查询后转换为 ECharts 所需的 `nodes / links / categories` 结构，节点大小按权重映射（`30 + weight × 20`），边带关系标签，前端直接渲染关系图。

**3. AI 诊断闭环与去重落库**
诊断流程：AI 出题 → 学生作答 → AI 提取薄弱点 → 写入 `learning_records`（掌握度初始 0.3）。写入前按「学生 + 薄弱点 + 当天」查询去重，避免同一天重复记录同一薄弱点。

**4. 完整的作业状态机**
`get_student_homeworks` 根据答题数、是否含未批改答案，动态计算四种状态（`pending / in_progress / submitted / completed`），并汇总得分与教师评语；教师批改后写入 `Notification` 表，学生端可查看消息。

**5. RBAC + 资源归属校验**
路由层用 `Depends(get_current_user)` 统一鉴权，学生接口一律基于当前用户 ID 查询自己的作业、笔记与通知，避免越权访问。

## 五、目录结构

```
XIAORUI/
├── backend/
│   ├── app/
│   │   ├── main.py                 # 应用入口、路由注册、静态资源挂载
│   │   ├── models.py               # 14 张表的 ORM 模型与 init_db()
│   │   ├── routers/                # 7 组路由：auth / student / teacher / admin / quiz / forum / ai_engine
│   │   └── services/doubao_ai.py   # 大模型调用封装（重试 / JSON 容错 / 降级）
│   └── requirements.txt
└── frontend/                       # Vue 3 前端工程
    └── src/                        # views / api / router / store
```

## 六、快速开始

**环境要求**：Python 3.9+、Node.js 20.19+ 或 22.12+

**1. 配置大模型密钥**
`backend/app/services/doubao_ai.py` 中的 API Key 已替换为占位符 `YOUR_DOUBAO_API_KEY`，请填入你的火山方舟密钥（或改为环境变量读取）。未配置时 AI 能力自动走内置兜底数据，不影响平台其他功能。

**2. 启动后端**

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- 服务地址：`http://localhost:8000`
- 接口文档（Swagger）：`http://localhost:8000/docs`
- 数据库：首次启动自动创建 `xiaorui_full_system.db`

**3. 启动前端**

```bash
cd frontend
npm install
npm run dev
```

## 七、说明

本项目为课程实践作品，大模型密钥等敏感配置已从代码中移除，请以占位符或环境变量方式注入后再运行。
