import streamlit as st
from langgraph_backend import graph
from langchain_core.messages import BaseMessage, HumanMessage
import uuid

# ********************** Utility Functions **********************
def get_thread_id():
    """Generate a unique thread ID."""
    return str(uuid.uuid4())

# ********************** Streamlit App Setup **********************

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {'configurable': {"thread_id": st.session_state.thread_id}}


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box
prompt = st.chat_input("Say something")


# ****************** Sidebar ******************
if "threads" not in st.session_state:
    st.session_state.threads = []

if st.session_state.thread_id not in st.session_state.threads:
    st.session_state.threads.append(st.session_state.thread_id)

st.sidebar.title("Langgraph Sidebar")
# New Chat
if st.sidebar.button("New Chat"):
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    if st.session_state.thread_id not in st.session_state.threads:
        st.session_state.threads.append(st.session_state.thread_id)

# Previous Conversations
st.sidebar.write("Previous Conversations")
for tid in st.session_state.threads:
    if st.sidebar.button(tid, key=tid):
        st.session_state.thread_id = tid
        st.session_state.messages = st.session_state.get(f"messages_{tid}", [])

# Save messages per thread
st.session_state[f"messages_{st.session_state.thread_id}"] = st.session_state.messages


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
                config= config,
                stream_mode= 'messages'
            )
        )

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})

