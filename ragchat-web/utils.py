import streamlit as st


def show_toast(message: str, success: bool = True):
    """
    显示一个通用的toast提示
    :param message: 提示小时内容
    :param success: 是否为成功消息,默认为True
    """
    icon = "√" if success else "⚠"
    st.toast(message, icon=icon)
