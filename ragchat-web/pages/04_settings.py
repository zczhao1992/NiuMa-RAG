import streamlit as st


st.title("设置")

tabs = st.tabs(['模型设置', '聊天记录', '通用提示词设置', 'RAG提示词设置', '检索设置'])


with tabs[0]:
    st.subheader('模型设置')

    st.selectbox("选择模型", ["openai", "deepseek"])
    st.slider("温度", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    st.text_input("API Key", type="password")

    st.text_input("API BASE URL", value="")

    st.button("保存")

with tabs[1]:
    st.subheader('聊天记录')

    st.selectbox("选择用户", ["用户A", "用户B", "用户C"])
    st.button("清除聊天记录")


with tabs[2]:
    st.subheader('通用提示词设置')
    st.text_area("系统提示词", value="你是一个只能帮助小助手，请回答用户问题")
    st.button("保存", key="base_save")

with tabs[3]:
    st.subheader('RAG提示词设置')
    st.text_area("RAG系统提示词", value="你是一个只能帮助小助手，请回答用户问题")
    st.button("保存", key="rag_save")

with tabs[4]:
    st.subheader('检索设置')
    search_mode = st.radio("检索方式", options=["向量检索", "全文检索", "混合检索"], index=0)

    if search_mode == "向量检索":
        st.slider("向量检索阈值", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    elif search_mode == "全文检索":
        st.slider("全文检索阈值", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    elif search_mode == "混合检索":
        st.slider("向量检索阈值", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
        st.slider("全文检索阈值", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

    st.number_input("TopN结果参数", min_value=1, max_value=10, value=5, step=1)
    st.button("保存", key="search_save")
