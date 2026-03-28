import asyncio
import streamlit as st
from api import update_collection


def save_to_backend(collection, name):
    asyncio.run(update_collection(collection["uuid"], name))
    st.success(f"名称 {name} 修改已保存到后端")
    return True


def main():
    st.title("修改空间")

    if "select_collection" not in st.session_state:
        st.switch_page("pages/02_space.py")
        return

    if st.session_state["select_collection"] is None:
        st.switch_page("pages/02_space.py")
        return

    name = st.text_input(
        "名称", value=st.session_state["select_collection"]["name"])

    col1, col2 = st.columns(2)

    with col1:
        if st.button("保存"):
            if name:
                result = save_to_backend(
                    st.session_state["select_collection"], name)
                if result:
                    st.switch_page("pages/02_space.py")
            else:
                st.error("请输入名称")

    with col2:
        if st.button("取消"):
            st.switch_page("pages/02_space.py")


main()
