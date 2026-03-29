import asyncio
import streamlit as st
from api import upload_file, get_collections
from utils import show_toast
# from hidden_pages import hide_pages

# hide_pages()

st.title("文件上传")

collection_list = {}
lists = asyncio.run(get_collections())  # 获取用户列表

if lists:
    for collection in lists:
        collection_list[collection["name"]] = collection["uuid"]

display_options = list(collection_list.keys())

if "selected_collection" not in st.session_state:
    st.session_state["selected_collection"] = display_options[0] if display_options else None

collection_name = st.selectbox(
    "归属空间",
    display_options,
    key="selected_collection"
)

uploaded_file = st.file_uploader("请上传文件", type=["txt", "docx", "pdf"])

if st.button("提交"):
    if uploaded_file is not None:
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            selected_collection_id = collection_list[st.session_state["selected_collection"]]
            response = asyncio.run(upload_file(selected_collection_id, files))
            show_toast(f"上传文件成功")
            st.switch_page("pages/03_rag.py")
        except Exception as e:
            show_toast(f"上传文件失败：{e}", False)
    else:
        st.warning("请先上传文件!")
