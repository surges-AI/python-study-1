import streamlit as st
import os
import json
import datetime
from openai import OpenAI

#页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def save():
    if st.session_state.session_id:
        # 构建新的会话对象
        session_data = {
            "session_id": st.session_state.session_id,
            "messages": st.session_state.messages,
            "name": st.session_state.name,
            "nature": st.session_state.nature
        }
        # 文件夹管理
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.session_id}.json", "w",encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

#加载所有会话列表
def load_sessions():
    session_list=[]
    if os.path.exists("sessions"):
        list=os.listdir("sessions")
        for file in list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    session_list.sort(reverse=True)
    return session_list

#加载指定会话信息
def load_session(session_id):
    try:
        if os.path.exists(f"sessions/{session_id}.json"):
            with open(f"sessions/{session_id}.json", "r",encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.name = session_data["name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.session_id = session_data["session_id"]
    except Exception:
        st.error("会话加载失败!")

#删除指定文件
def delete_file(file_name):
    try:
        if os.path.exists(f"sessions/{file_name}.json"):
            os.remove(f"sessions/{file_name}.json")
            if st.session_state.session_id== file_name:
                st.session_state.messages=[]
                st.session_state.session_id=generate_session_id()

    except Exception:
        st.error("删除失败!")


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
#会话标识
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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
    st.subheader("AI控制面板")

    if st.button("新建会话",width="stretch",icon="🌏"):
        #保存会话信息
        save()

        #创建新的会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save()
            st.rerun()

    #会话历史
    st.text("会话历史")
    session_list=load_sessions()
    for session in session_list:
        col1,col2=st.columns([4,1])
        with col1:
            #加载会话
            if st.button(session, key=session, width="stretch", icon="📄",type="primary" if st.session_state.session_id==session else "secondary"):
                load_session(session)
                st.rerun()
            #删除会话
        with col2:
            if st.button("", key=f"de{session}", width="stretch", icon="❌"):
                delete_file(session)
                st.rerun()

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

    #保存会话信息
    st.session_state.messages.append({"role": "assistant", "content": h})
    save()