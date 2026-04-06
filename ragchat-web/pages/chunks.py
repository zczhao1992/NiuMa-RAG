import asyncio
import streamlit as st
import pandas as pd
from api import get_chunks
from utils import show_toast
from hidden_pages import hide_pages

hide_pages()

if "select_file" not in st.session_state:
    st.switch_page("pages/03_rag.py")

if st.session_state["select_file"] is None:
    st.switch_page("pages/03_rag.py")

st.title("文件片段")
st.header(f"文件名：{st.session_state["select_file"]["file_name"]}")

data = {
    "编号": [],
    "片段": [],
    "序号": [],
    "向量状态": [],
    "创建时间": []
}

chunks = asyncio.run(get_chunks(st.session_state["select_file"]["uuid"]))

if chunks:
    for chunk in chunks:
        data["编号"].append(chunk["uuid"])
        data["片段"].append(chunk["context"])
        data["序号"].append(chunk["index"])
        data["创建时间"].append(chunk["create_time"])
        if chunk["status"] == 1:
            data["向量状态"].append("已向量")
        else:
            data["向量状态"].append("进行中")

df = pd.DataFrame(data)
event = {}

with st.container():
    col1, col2, col3 = st.columns([12, 2, 1])
    with col2:
        st.button("关联问题")
    with col3:
        if st.button("返回"):
            st.switch_page("pages/03_rag.py")

event = st.dataframe(df,
                     use_container_width=True,
                     key="data",
                     hide_index=True,
                     selection_mode=['single-row'],
                     on_select='rerun')

if len(event.selection["rows"]) > 0:
    st.session_state["select_chunk_index"] = event.selection["rows"][0]
else:
    st.session_state["select_chunk_index"] = None
    st.session_state["select_chunk"] = None
