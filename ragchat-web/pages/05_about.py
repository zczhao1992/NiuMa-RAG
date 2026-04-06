import streamlit as st
from hidden_pages import hide_pages

# 隐藏不需要的页面
hide_pages()

# 页面标题
st.title("💡 关于 NiuMa RAG")

st.markdown("---")

# 1. 项目简介
st.header("🌟 项目概述")
st.markdown("""
**NiuMa RAG** 是一款专注于企业级知识管理的 **检索增强生成（RAG）** 助手。
它能够像“牛马”一样勤恳地消化你上传的各类文档，通过先进的向量检索技术，在海量数据中精准定位答案，并结合大语言模型（LLM）为你提供专业、可靠的回答。

* **精准检索**：支持向量、全文及混合搜索。
* **高效管理**：灵活的知识空间（Namespace）隔离，确保数据井然有序。
* **持久记忆**：基于 Postgres 的聊天记录存储，对话上下文永不丢失。
""")

st.markdown("---")

# 2. 快速上手指南
st.header("🚀 快速使用指南")

# 使用 info 组件突出显示演示账号和空间
st.info("如果你是第一次使用，可以按照以下配置快速体验系统的 RAG 能力：")

col1, col2 = st.columns(2)

with col1:
    st.success("**默认知识空间**")
    st.markdown("""
    - **空间名称**：`养生知识`
    - **内容简介**：内置了养生的相关内容。
    """)

with col2:
    st.warning("**演示用户账号**")
    st.markdown("""
    - **用户名**：`zc`
    - **说明**：使用该 ID 登录或进行对话，即可关联已有的聊天记忆。
    """)

st.markdown("""
### 🛠️ 如何开始对话？
1.  前往 **[知识库]** 页面。
2.  在侧边栏选择知识空间：`养生知识`。
3.  输入你的用户 ID：`zc`。
4.  开始提问，例如：“*减肥的危害有哪些？*”
""")

st.markdown("---")

# 3. 技术栈
with st.expander("🛠️ 查看技术架构"):
    st.markdown("""
    - **Frontend**: Streamlit
    - **Backend**: FastAPI / LangChain
    - **Database**: Neon Postgres (Vector / SQL)
    - **LLM**: DeepSeek / OpenAI 
    - **Driver**: Psycopg (Synchronous Mode for stability)
    """)

# 页脚
st.caption("© 2026 NiuMa RAG - 让知识触手可及，让牛马不再加班。")
