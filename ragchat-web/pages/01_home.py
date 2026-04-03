import asyncio
import streamlit as st
import pandas as pd
from api import get_users, chat, get_collections
from base_message import HumanMessage, AIMessage

st.set_page_config(page_title="首页", page_icon=":bar_chart:", layout="wide")


st.markdown("""
<style>
:root {
    --sidebar-width: 21rem;      /* 展开宽度 */
    --sidebar-collapsed: 3.5rem; /* 收起宽度 */
    --input-h: 84px;
}

/* 给正文留出底部空间 */
.main .block-container {
    padding-bottom: calc(var(--input-h) + 24px);
}

/* 默认按“收起侧栏”计算 */
.st-key-input_container {
    position: fixed;
    bottom: 0;
    left: var(--sidebar-collapsed);
    width: calc(100vw - var(--sidebar-collapsed));
    z-index: 9999;

    box-sizing: border-box;   /* 防止 padding 撑爆宽度 */
    padding: 10px 16px;
    border-top: 1px solid #e5e7eb;
    background: rgba(255, 255, 255, 0.98);

    overflow-x: hidden;       /* 兜底，避免横向滚动 */
}

/* 侧栏展开时，改用展开宽度 */
div[data-testid="stAppViewContainer"]:has(section[data-testid="stSidebar"][aria-expanded="true"]) .st-key-input_container {
    left: var(--sidebar-width);
    width: calc(100vw - var(--sidebar-width));
}

/* 内层不要再额外撑宽 */
.st-key-input_container > div {
    width: 100%;
    max-width: 100%;
    margin: 0;
}

/* 小屏幕下直接铺满，避免计算误差 */
@media (max-width: 900px) {
    .st-key-input_container {
        left: 0;
        width: 100vw;
    }
}
</style>
""", unsafe_allow_html=True)

top_container = st.container()

chat_container = st.container()

input_container = st.container(key="input_container")

# 获取用户列表
user_list = {}
users = asyncio.run(get_users())

if users:
    user_list = {user["name"]: user["id"] for user in users}

user_display_options = list(user_list.keys())


collection_list = {}
collections = asyncio.run(get_collections())
if collections:
    collection_list = {collection["name"]: collection["uuid"]
                       for collection in collections}
collection_display_options = list(collection_list.keys())
collection_display_options.insert(0, "选择知识空间")

with top_container:
    st.selectbox(label="选择知识空间",
                 options=collection_display_options,
                 key="home_selected_collection",
                 label_visibility="collapsed",
                 index=None,
                 placeholder="请选择知识空间")


def handle_user_input():
    user_input = st.session_state.get("user_input", "")
    selected_user_id = user_list[st.session_state["selected_user"]]

    if user_input:
        user_message_key = "messages-" + selected_user_id
        st.session_state[user_message_key].append(
            HumanMessage(content=user_input))

        if st.session_state["home_selected_collection"] == "选择知识空间":
            selected_collection_id = ""
        else:
            selected_collection_id = collection_list[st.session_state["home_selected_collection"]]

        ai_message = asyncio.run(
            chat(selected_user_id, user_input, selected_collection_id))
        if ai_message is None:
            st.session_state[user_message_key].append(
                AIMessage(content="AI 消息获取失败"))
        else:
            st.session_state[user_message_key].append(
                AIMessage(content=ai_message["content"]))


async def show_chat_message(user_id: str):
    chat_container.empty()
    user_message_key = "messages-" + user_id
    if user_message_key not in st.session_state:
        st.session_state[user_message_key] = []
    with chat_container:
        for message in st.session_state[user_message_key]:
            if isinstance(message, HumanMessage):
                with st.chat_message('user'):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message('assistant'):
                    st.markdown(message.content)

if "selected_user" not in st.session_state:
    st.session_state["selected_user"] = user_display_options[0] if user_display_options else None

asyncio.run(show_chat_message(user_list[st.session_state["selected_user"]]))

with input_container:
    col1, col2 = st.columns([1, 9], gap='small')

    with col1:
        st.selectbox(
            label="用户选择",
            options=user_display_options,
            key="selected_user",
            label_visibility='collapsed'
        )
    with col2:
        st.chat_input(
            f"{st.session_state["selected_user"]}说: 请输入信息...",
            key="user_input",
            on_submit=handle_user_input
        )
