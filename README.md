# 🐂 NiuMa RAG: 企业级知识库检索增强生成系统

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

> **"让知识触手可及，让牛马不再加班。"** > **NiuMa RAG** 是一款基于异步后端与流式前端构建的全文/向量混合检索问答系统，旨在帮助团队快速构建私有知识库，实现智能化的文档交互。

---

## ✨ 项目特性

- **🔍 混合检索增强 (Hybrid Search)**：结合 **PGVector** 向量检索与 PostgreSQL 全文搜索，支持 RRF 重排序算法，确保在复杂语境下的回答精准度。
- **📂 知识空间隔离 (Multi-Namespace)**：支持多知识空间管理，不同项目或业务数据物理/逻辑隔离，互不干扰。
- **💬 持久化对话记忆**：底层集成 Postgres 存储聊天记录，完美支持多轮对话上下文关联，告别“断片式”聊天。
- **⚡ 异步流式响应**：基于 FastAPI 与 SSE（Server-Sent Events）技术，前端提供极致流畅的打字机对话体验。
- **🛠️ 易于扩展**：插件化 LLM 接入层，支持 DeepSeek、OpenAI、Claude 及本地 Llama 等多种主流模型。

---

## 🏗️ 技术架构

项目采用前后端分离架构，针对 Windows 开发环境进行了驱动层优化：

- **前端 (Frontend)**: Streamlit - 响应式交互界面，支持多页面导航。
- **后端 (Backend)**: FastAPI - 高性能异步 Web 框架。
- **编排 (Orchestration)**: LangChain - 灵活的 LLM 工作流调度与提示词工程。
- **数据库 (Database)**: **Neon Postgres** (Vector + Fulltext) - 云原生 Serverless 数据库解决方案。
- **驱动层 (Driver)**: Psycopg (Sync Mode) - 解决 Windows 环境下协程循环冲突，提供极致稳定性。

---

## 🚀 快速上手

### 1. 克隆仓库

```bash
git clone [https://github.com/your-username/NiuMa-RAG.git](https://github.com/your-username/NiuMa-RAG.git)
cd NiuMa-RAG

```

### 2. 环境配置

```bash
在 ragchat-server 目录下创建 .env 文件，并填入你的配置：
DATABASE_URL=postgresql://user:password@host/neondb?sslmode=require
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here

```

### 3. 启动后端服务

```bash
cd ragchat-server

# 使用 uv 一键安装依赖并运行
uv pip install -r requirements.txt
uv run main.py

# 或者使用传统方式：
# pip install -r requirements.txt && python main.py

```

### 4. 启动前端界面

```bash
cd ragchat-client

# 使用 uv 一键安装依赖并运行
uv pip install -r requirements.txt
uv run streamlit run app.py

# 或者使用传统方式：
# pip install -r requirements.txt && streamlit run app.py

```
