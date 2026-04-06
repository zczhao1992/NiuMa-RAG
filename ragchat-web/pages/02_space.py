import asyncio
import streamlit as st
import pandas as pd
from api import get_collections, delete_collection_by_id
from hidden_pages import hide_pages

hide_pages()

st.title("知识空间")

data = {
    "编号": [],
    "名称": [],
    "创建时间": []
}

collections = asyncio.run(get_collections())

if collections:
    for collection in collections:
        data["编号"].append(collection["uuid"])
        data["名称"].append(collection["name"])
        data["创建时间"].append(collection["create_time"])

df = pd.DataFrame(data)


@st.dialog("确认删除")
def confirm_delete(name, uuid):
    st.write(f"您确定要删除 **{name}** 吗？此操作不可恢复")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("确认删除", type="primary"):
            asyncio.run(delete_collection_by_id(uuid))
            st.rerun()
    with col2:
        if st.button("取消"):
            st.rerun()


with st.container():
    col1, col2, col3, col4 = st.columns([10, 2, 2, 2])
    with col2:
        if st.button("新建"):
            st.switch_page("pages/namespace_add.py")
    with col3:
        if st.button("编辑"):
            if st.session_state["select_collection_index"] is not None:
                print(
                    f"{collections[st.session_state["select_collection_index"]]}")
                st.session_state["select_collection"] = collections[st.session_state["select_collection_index"]]
                st.switch_page("pages/namespace_update.py")
    with col4:
        if st.button("删除"):
            if st.session_state["select_collection_index"] is not None:
                selected_collection = collections[st.session_state["select_collection_index"]]
                confirm_delete(
                    selected_collection["name"], selected_collection["uuid"])

event = st.dataframe(df,
                     use_container_width=True,
                     key="data",
                     hide_index=True,
                     selection_mode=['single-row'],
                     on_select='rerun')


if len(event.selection["rows"]) > 0:
    st.session_state["select_collection_index"] = event.selection["rows"][0]
else:
    st.session_state["select_collection_index"] = None
    st.session_state["select_collection"] = None
