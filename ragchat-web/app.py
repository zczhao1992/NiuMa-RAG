import base64
import streamlit as st


logo_svg = """
<svg width="400" height="60" xmlns="http://www.w3.org/2000/svg">
  <text x="50%" y="50%" font-family="Microsoft YaHei, sans-serif" font-size="52" fill="#ff4b4b" text-anchor="middle" dominant-baseline="middle" font-weight="bold">
    NiuMa RAG
  </text>
</svg>
"""


def get_svg_base64(svg_str):
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_str.encode()).decode()}"


st.logo(get_svg_base64(logo_svg))

pg = st.navigation([
    st.Page("pages/01_home.py", title="首页"),
    st.Page("pages/02_space.py", title="知识空间"),
    st.Page("pages/03_rag.py", title="知识库"),
    st.Page("pages/04_settings.py", title="设置"),
    st.Page("pages/05_about.py", title="关于"),
    st.Page("pages/namespace_add.py", title="新建知识空间"),
    st.Page("pages/namespace_update.py", title="编辑知识空间"),
    st.Page("pages/file_upload.py", title="上传文件"),
    st.Page("pages/chunks.py", title="查看片段"),
])

pg.run()
