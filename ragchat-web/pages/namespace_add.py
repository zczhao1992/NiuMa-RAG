import asyncio
import streamlit as st
from api import create_collection


def save_to_backend(name):
    asyncio.run(create_collection(name))
    st.success(f"名称 {name} 已保存到后端")
    return True


def main():
    st.title("新建空间")

    name = st.text_input("名称")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("保存"):
            if name:
                result = save_to_backend(name)
                if result:
                    st.switch_page("pages/02_space.py")
            else:
                st.error("请输入名称")

    with col2:
        if st.button("取消"):
            st.switch_page("pages/02_space.py")


main()
