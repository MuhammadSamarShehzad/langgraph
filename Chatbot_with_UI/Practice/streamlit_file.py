import streamlit as st
import uuid
from langgraph_file import graph, retrieve_all_threads, load_conversation
from langchain_core.messages import HumanMessage, AIMessage

# ---------- Utilities ----------
def create_new_thread():
    new_id = str(uuid.uuid4())[:7]
    st.session_state["thread_id"] = new_id
    st.session_state["message_history"] = []
    if new_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(new_id)

# ---------- Session Initialization ----------
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = str(uuid.uuid4())[:7]

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

# ensure current thread is in list
if st.session_state["thread_id"] not in st.session_state["chat_threads"]:
    st.session_state["chat_threads"].append(st.session_state["thread_id"])

# ---------- Sidebar ----------
st.sidebar.title("LangGraph Chatbot")
if st.sidebar.button("➕ New Chat"):
    create_new_thread()
    st.rerun()

st.sidebar.header("Previous Chats")
for tid in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(tid), key=f"btn_{tid}"):
        st.session_state["thread_id"] = tid
        messages = load_conversation(tid)
        print(f"\n\n\n\nmessages are:\n{messages}")

        st.session_state["message_history"] = [
            {
                "role": "human" if isinstance(m, HumanMessage) else "ai",
                "content": m.content
            }
            for m in messages
        ]
        st.rerun()

# ---------- Main Chat Display ----------
st.subheader(f"Chat: {st.session_state['thread_id']}")

if not st.session_state["message_history"]:
    st.info("No messages in this thread yet.")
else:
    for msg in st.session_state["message_history"]:
        with st.chat_message(msg["role"]):
            st.text(msg["content"])

# ---------- Chat Input ----------
user_input = st.chat_input("Say something")
if user_input:
    # append user message
    st.session_state["message_history"].append({"role": "human", "content": user_input})
    with st.chat_message("human"):
        st.text(user_input)

    # call LangGraph
    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    response = graph.invoke({"messages": HumanMessage(content=user_input)}, config=CONFIG)
    answer = response["messages"][-1].content

    # append AI message
    st.session_state["message_history"].append({"role": "ai", "content": answer})
    with st.chat_message("ai"):
        st.text(answer)
