import os
import sqlite3
from dotenv import load_dotenv
from typing import TypedDict, Annotated

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

# ---------- LLM ----------
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_base="https://router.huggingface.co/v1",
    openai_api_key=api_key,
    model_name="openai/gpt-oss-120b:cerebras",
)

# ---------- LangGraph Setup ----------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    input_messages = state["messages"]
    response = llm.invoke(input_messages)
    return {"messages": [AIMessage(content=response.content)]}

# SQLite connection and checkpointer
conn = sqlite3.connect("practice.db", check_same_thread=False, isolation_level=None)
checkpointer = SqliteSaver(conn=conn)

graph_workflow = StateGraph(ChatState)
graph_workflow.add_node("chat_node", chat_node)
graph_workflow.add_edge(START, "chat_node")
graph_workflow.add_edge("chat_node", END)

graph = graph_workflow.compile(checkpointer=checkpointer)

# ---------- Utilities ----------
def retrieve_all_threads():
    """Return list of all thread IDs stored in DB"""
    thread_ids = set()
    for checkpoint in checkpointer.list(None):
        thread_ids.add(checkpoint.config["configurable"]["thread_id"])
    return list(thread_ids)


def load_conversation(thread_id):
    """Return list of messages (HumanMessage/AIMessage) for a thread"""
    state = graph.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])
