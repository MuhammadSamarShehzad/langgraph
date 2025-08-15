import streamlit as st
import time
from langgraph_file import graph
from langchain_core.messages import HumanMessage

thread_id = "t_1"

if "threads" not in st.session_state:
    st.session_state["threads"] = {}


if thread_id not in st.session_state["threads"]:
    st.session_state["threads"][thread_id] = []

# Display all messages in the current thread
for msg in st.session_state["threads"][thread_id]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


prompt = st.chat_input("Say something")
config = {'configurable': {"thread_id": "t_1"}}

if prompt:

    with st.chat_message("human"):
        st.session_state["threads"][thread_id].append({"role": "human", "content": prompt})
        st.write(prompt)

    with st.chat_message("ai"):
        response = graph.invoke({"messages": [HumanMessage(content=prompt)]},
             config=config)
        st.session_state["threads"][thread_id].append({"role": "ai", "content": response["messages"][-1].content})

        st.write(response["messages"][-1].content)