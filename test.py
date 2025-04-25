import streamlit as st
from langchain_openai import ChatOpenAI

# 设置Streamlit应用标题
st.title("与 GPT-4o 的简单对话")

# 在侧边栏设置 OpenAI API 密钥输入框
openai_api_key = st.sidebar.text_input("OpenAI API 密钥", type="password")

# 初始化 OpenAI 模型
if openai_api_key:
    llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key)

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "您好！有什么我可以帮您？"}]

    # 显示聊天记录
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 用户输入框
    if prompt := st.chat_input("请输入您的问题"):
        # 将用户输入添加到聊天记录
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用 OpenAI 模型获取回复
        full_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            for chunk in llm.stream(st.session_state["messages"]):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        # 将模型回复添加到聊天记录
        st.session_state["messages"].append({"role": "assistant", "content": full_response})

else:
    st.warning("请在侧边栏输入您的 OpenAI API 密钥。")