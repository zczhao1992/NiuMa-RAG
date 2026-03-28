import streamlit as st

pg = st.navigation([
    st.Page("pages/01_home.py", title="首页"),
    st.Page("pages/02_space.py", title="知识空间"),
    st.Page("pages/03_rag.py", title="知识库"),
    st.Page("pages/04_settings.py", title="设置"),
    st.Page("pages/05_about.py", title="关于"),
    st.Page("pages/namespace_add.py", title="新建"),
    st.Page("pages/namespace_update.py", title="编辑"),
])

pg.run()
