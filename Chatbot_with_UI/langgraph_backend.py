from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    openai_api_base="https://router.huggingface.co/v1",
    openai_api_key=api_key,
    model_name="openai/gpt-oss-120b:cerebras",
)

from typing import TypedDict, Annotated
class Agent(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_with_llm(state: Agent):
    input_messages = state["messages"]
    response = llm.invoke(input_messages).content
    return {"messages": [response]}

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

workflow = StateGraph(Agent)

workflow.add_node("chat_with_llm", chat_with_llm)

workflow.add_edge(START, "chat_with_llm")
workflow.add_edge("chat_with_llm", END)

checkpointer = InMemorySaver()

graph = workflow.compile(checkpointer=checkpointer)
