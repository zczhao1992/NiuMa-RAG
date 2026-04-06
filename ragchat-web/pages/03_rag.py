import asyncio
import streamlit as st
import pandas as pd
from api import get_files, delete_file
from hidden_pages import hide_pages

hide_pages()

st.title("知识库")


data = {
    "编号": [],
    "文件名": [],
    "文件类型": [],
    "归属空间": [],
    "创建时间": []
}

files = asyncio.run(get_files(""))

if files:
    for file in files:
        data["编号"].append(file["uuid"])
        data["文件名"].append(file["file_name"])
        data["文件类型"].append(file["file_extension"])
        data["归属空间"].append(file["collection_id"])
        data["创建时间"].append(file["create_time"])


df = pd.DataFrame(data)


@st.dialog("确认删除")
def confirm_delete(name, uuid):
    st.write(f"您确定要删除 **{name}** 吗？此操作不可恢复")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("确认删除", type="primary"):
            asyncio.run(delete_file(uuid))
            st.rerun()
    with col2:
        if st.button("取消"):
            st.rerun()


with st.container():
    col1, col2, col3, col4 = st.columns([10, 4, 4, 2])
    with col2:
        if st.button("上传文件"):
            st.switch_page("pages/file_upload.py")
    with col3:
        if st.button("查看片段"):
            if st.session_state["select_file_index"] is not None:
                print(f"{files[st.session_state["select_file_index"]]}")
                st.session_state["select_file"] = files[st.session_state["select_file_index"]]
                st.switch_page("pages/chunks.py")
    with col4:
        if st.button("删除"):
            if st.session_state["select_file_index"] is not None:
                selceted_file = files[st.session_state["select_file_index"]]
                confirm_delete(
                    selceted_file["file_name"], selceted_file["uuid"])


event = st.dataframe(df,
                     use_container_width=True,
                     key="data",
                     hide_index=True,
                     selection_mode=['single-row'],
                     on_select='rerun')


if len(event.selection["rows"]) > 0:
    st.session_state["select_file_index"] = event.selection["rows"][0]
else:
    st.session_state["select_file_index"] = None
    st.session_state["select_file"] = None
