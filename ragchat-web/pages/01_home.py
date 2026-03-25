import streamlit as st

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


with top_container:
    st.selectbox(label="选择知识空间",
                 options=("空间A", "空间B", "空间C"),
                 index=None,
                 placeholder="请选择知识空间")


with chat_container:
    with st.chat_message('user'):
        st.markdown("你好")
    with st.chat_message('assistant'):
        st.markdown("我是AI")

with input_container:
    col1, col2 = st.columns([1, 9], gap='small')

    with col1:
        st.selectbox(
            label="用户选择",
            options=["用户1", "用户2", "用户3"],
            label_visibility='collapsed'
        )
    with col2:
        st.chat_input('请输入信息')
