import asyncio
import streamlit as st
from api import batch_upsert_dicts, get_dict, get_users, clear_chat_history

from utils import show_toast
from hidden_pages import hide_pages

hide_pages()

st.set_page_config(page_title="设置", layout="wide")
st.title("设置")

st.session_state["llm_model"] = asyncio.run(get_dict("llm_model", "openai"))
st.session_state["OPENAI_API_KEY"] = asyncio.run(
    get_dict("openai_api_key", ""))
st.session_state["OPENAI_API_BASE"] = asyncio.run(
    get_dict("openai_api_base", ""))
st.session_state["DEEPSEEK_API_KEY"] = asyncio.run(
    get_dict("deepseek_api_key", ""))
st.session_state["PROMPT_SYSTEM"] = asyncio.run(get_dict("prompt_system", ""))
st.session_state["PROMPT_SYSTEM_RAG"] = asyncio.run(
    get_dict("prompt_system_rag", ""))
# st.session_state["TEMPERATURE"] = asyncio.run(
#     get_dict("temperature", 0.5))
temp_val = asyncio.run(get_dict("temperature", "0.5"))
st.session_state["TEMPERATURE"] = float(temp_val) if temp_val else 0.5

current_search_mode = asyncio.run(get_dict("search_mode", "embedding"))
threshold_vector = float(asyncio.run(
    get_dict("threshold_vector", "0.5")))
threshold_fulltext = float(asyncio.run(
    get_dict("threshold_fulltext", "0.05")))
# top_n_d = float(asyncio.run(
#     get_dict("top_n", "0.05")))

raw_top_n = asyncio.run(get_dict("top_n", "5"))
top_n_d = int(float(raw_top_n))

tabs = st.tabs(['模型设置', '聊天记录', '通用提示词设置', 'RAG提示词设置', '检索设置'])


with tabs[0]:
    st.subheader('模型设置')

    default_model_index = 0 if st.session_state["llm_model"] == "openai" else 1

    model_type = st.selectbox(
        "选择模型", ["openai", "deepseek"], index=default_model_index)
    temperature = st.slider("温度", min_value=0.0,
                            max_value=1.0, value=st.session_state["TEMPERATURE"], step=0.1)

    if model_type == "openai":
        open_ai_key = st.text_input(
            "open_ai_key", value=st.session_state["OPENAI_API_KEY"], max_chars=None, key=None, type="password")

        open_ai_base = st.text_input(
            "open_ai_base", value=st.session_state["OPENAI_API_BASE"], max_chars=None, key=None, type="default")

        saved = st.button("保存", key="save_openai")

        if saved:
            data = [
                {"key": "open_ai_key", "value": open_ai_key},
                {"key": "open_ai_base", "value": open_ai_base},
                {"key": "llm_model", "value": "openai"},
                {"key": "temperature", "value": str(temperature)},
            ]
            result = asyncio.run(batch_upsert_dicts(data))

            if result:
                st.session_state["OPENAI_API_KEY"] = open_ai_key
                st.session_state["OPENAI_API_BASE"] = open_ai_base
                show_toast("OpenAI 配置已保存！")
            else:
                show_toast("保存OpenAI配置失败", False)

    elif model_type == "deepseek":
        deepseek_api_key = st.text_input(
            "deepseek_api_key", value=st.session_state["DEEPSEEK_API_KEY"], max_chars=None, key=None, type="password")
        saved = st.button("保存", key="save_deepseek")

        if saved:
            data = [
                {"key": "deepseek_api_key", "value": deepseek_api_key},
                {"key": "llm_model", "value": "deepseek"},
                {"key": "temperature", "value": str(temperature)},
            ]
            result = asyncio.run(batch_upsert_dicts(data))

            if result:
                st.session_state["DEEPSEEK_API_KEY"] = deepseek_api_key

                show_toast("deepseek 配置已保存！")
            else:
                show_toast("保存deepseek配置失败", False)
with tabs[1]:
    st.subheader('清除聊天记录')
    user_list = {}

    lists = asyncio.run(get_users())
    if lists:
        for user in lists:
            user_list[user["name"]] = user["id"]

    display_options = list(user_list.keys())

    if "selected_clear_user" not in st.session_state:
        st.session_state["selected_clear_user"] = display_options[0] if display_options else user_list[0]

    st.selectbox("选择用户",
                 display_options,
                 key="selected_clear_user",
                 label_visibility="collapsed"
                 )

    if st.button("清除聊天记录"):
        selected_user_id = user_list[st.session_state["selected_clear_user"]]
        asyncio.run(clear_chat_history(user_id=selected_user_id))
        show_toast("清除聊天记录成功！")

with tabs[2]:
    st.subheader('系统提示词模版')
    prompt_system = st.text_area(
        "系统提示词", value=st.session_state["PROMPT_SYSTEM"], key="text_prompt_system", height=200, max_chars=None)
    if st.button("保存", key="save_prompt_system"):
        data = [
            {"key": "prompt_system", "value": prompt_system}
        ]
        result = asyncio.run(batch_upsert_dicts(data))
        if result:
            st.session_state["PROMPT_SYSTEM"] = prompt_system
            show_toast("系统提示词模版配置成功！")
        else:
            show_toast("系统提示词模版配置失败！", False)

with tabs[3]:
    st.subheader('RAG提示词设置')
    prompt_system_rag = st.text_area(
        "RAG系统提示词", value=st.session_state["PROMPT_SYSTEM_RAG"], key="text_prompt_system_rag", height=200, max_chars=None)
    if st.button("保存", key="save_prompt_system_rag"):
        data = [
            {"key": "prompt_system_rag", "value": prompt_system_rag}
        ]
        result = asyncio.run(batch_upsert_dicts(data))
        if result:
            st.session_state["PROMPT_SYSTEM_RAG"] = prompt_system_rag
            show_toast("RAG提示词模版配置成功！")
        else:
            show_toast("RAG提示词模版配置失败！", False)

with tabs[4]:
    st.subheader('检索设置')

    search_mode_value_map = {
        "向量检索": "embedding",
        "全文检索": "fulltext",
        "混合检索": "hybrid"
    }

    search_mode_display_map = {
        "embedding": "向量检索",
        "fulltext": "全文检索",
        "hybrid": "混合检索"
    }

    display_mode = search_mode_display_map.get(current_search_mode, "向量检索")

    if "search_mode" not in st.session_state:
        st.session_state["search_mode"] = display_mode

    search_mode = st.radio(
        "选择检索方式", options=["向量检索", "全文检索", "混合检索"], key="search_mode", index=0)

    if search_mode == "向量检索":
        threshold_vector = st.slider(
            "向量检索阈值(越大越宽松)", min_value=0.0, max_value=1.0, value=threshold_vector, step=0.01)
        threshold_fulltext = None
    elif search_mode == "全文检索":
        threshold_fulltext = st.slider("全文检索阈值(越小越宽松)", min_value=0.00,
                                       max_value=1.00, value=threshold_fulltext, step=0.01)
        threshold_vector = None
    elif search_mode == "混合检索":
        threshold_vector = st.slider(
            "向量检索阈值(越大越宽松)", min_value=0.0, max_value=1.0, value=threshold_vector, step=0.01)
        threshold_fulltext = st.slider(
            "全文检索阈值(越小越宽松)", min_value=0.00, max_value=1.00, value=threshold_fulltext, step=0.01)

    top_n = st.number_input("TopN结果参数", min_value=1,
                            max_value=10, value=top_n_d, step=1)

    if st.button("保存", key="save_search_mode"):
        data = [
            {"key": "search_mode",
                "value": search_mode_value_map[search_mode]},
            {"key": "top_n", "value": str(top_n)},
            {"key": "threshold_vector",
                "value": "" if threshold_vector is None else str(threshold_vector)},
            {"key": "threshold_fulltext",
                "value":  "" if threshold_fulltext is None else str(threshold_fulltext)},
        ]

        result = asyncio.run(batch_upsert_dicts(data))
        if result:
            show_toast("检索设置已保存")
        else:
            show_toast("保存检索设置失败", False)
