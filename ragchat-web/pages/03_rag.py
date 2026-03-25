import streamlit as st
import pandas as pd

st.title("知识库")


data = {
    "编号": ["1", "2", "3"],
    "文件名": ["文件名1", "文件名2", "文件名3"],
    "文件类型": ["txt", "pdf", "doc"],
    "归属空间": ["空间1", "空间2", "空间3"],
    "创建时间": ["2021-01-01 00:00:00", "2021-01-01 00:00:00", "2021-01-01 00:00:00"]
}

df = pd.DataFrame(data)


with st.container():
    col1, col2, col3, col4 = st.columns([10, 2, 2, 2])
    with col2:
        st.button("上传文件")
    with col3:
        st.button("查看片段")
    with col4:
        st.button("删除")


event = st.dataframe(df, hide_index=True, selection_mode=[
    'single-row'], on_select='rerun')
