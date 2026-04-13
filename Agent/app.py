import time

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from react_agent import ReactAgent


st.title("智能问答服务助手")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"]=ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"]=[]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#用户输入提示词
prompt=st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    responses_messages=[]
    with st.spinner("智能客服思考中..."):
        res_stream=st.session_state["agent"].execute_stream(prompt)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream,responses_messages))
        st.session_state["message"].append({"role":"assistant","content":responses_messages[-1]})
        st.rerun()