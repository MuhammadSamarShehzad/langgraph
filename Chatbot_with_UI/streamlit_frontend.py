import streamlit as st
from langgraph_backend import graph
from langchain_core.messages import BaseMessage, HumanMessage

config = {'configurable': {"thread_id": 1}}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
prompt = st.chat_input("Say something")

# Add and display new messages
if prompt:
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.write(prompt)


    # response = f"{prompt}"  # Placeholder for assistant response
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in graph.stream(
                {'messages': [HumanMessage(content=prompt)]},
                config= {'configurable': {'thread_id': 'thread-1'}},
                stream_mode= 'messages'
            )
        )

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})

