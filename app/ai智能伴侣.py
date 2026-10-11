import streamlit as st
import os
from openai import OpenAI

#页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

system_prompt = """你的昵称为%s，性格为%s，请根据上文进行回复"""

#大标题
st.title("AI智能伴侣")

#判断是否存在
if "messages" not in st.session_state:
    st.session_state.messages = []
if "name" not in st.session_state:
    st.session_state.name = ""
if "nature" not in st.session_state:
    st.session_state.nature = ""

#展示聊天记录
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#侧边栏
with st.sidebar:
    st.subheader("AI信息")
    name=st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.name)
    if name:
        st.session_state.name = name
    nature=st.text_area("性格", placeholder="请输入性格",height=100,value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

#输入框
input_text = st.chat_input("Say something", submit_mode="stop")
if input_text:
    st.chat_message("user").write(input_text)
    st.session_state.messages.append({"role": "user", "content": input_text})
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt %(st.session_state.name,st.session_state.nature)},
            *st.session_state.messages
        ],
        stream=True
    )
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    res = st.empty()
    h = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            h += content
            res.chat_message("assistant").write(h)
    if h:
        st.session_state.messages.append({"role": "assistant", "content": h})
