from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages


llm = ChatOpenAI(
    openai_api_key="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",
    openai_api_base="https://openrouter.ai/api/v1",
    model="qwen/qwen3-30b-a3b:free"
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

# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict, Annotated
# from langchain_core.messages import BaseMessage
# from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import InMemorySaver
# from langgraph.graph.message import add_messages
# from dotenv import load_dotenv

# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# def chat_node(state: ChatState):
#     messages = state['messages']
#     response = llm.invoke(messages).content
#     return {"messages": [response]}

# # Checkpointer
# checkpointer = InMemorySaver()

# graph = StateGraph(ChatState)
# graph.add_node("chat_node", chat_node)
# graph.add_edge(START, "chat_node")
# graph.add_edge("chat_node", END)

# chatbot = graph.compile(checkpointer=checkpointer)





# import os

# if not os.environ.get("TAVILY_API_KEY"):
#     os.environ["TAVILY_API_KEY"] = "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"

# from langchain_core.tools import tool
# from langchain_core.messages import BaseMessage, AIMessage
# from langgraph.graph.message import add_messages
# from langchain_tavily import TavilySearch
# from langchain.agents import initialize_agent, AgentType
# from typing import TypedDict, Annotated

# # --- Define tool ---
# tavily_tool_instance = TavilySearch(
#     max_results=2,
#     topic="general",
#     include_raw_content=False,
#     search_depth="advanced"
# )

# @tool
# def tavily_search(query: str) -> str:
#     """Search the web for recent and relevant information."""
#     result = tavily_tool_instance.invoke({"query": query})
#     return result["results"][0]["content"] if result["results"] else "No relevant info found."

# # --- Define LLM and agent ---
# from langchain.chat_models import ChatOpenAI

# llm = ChatOpenAI(
#     model="mistral-medium",
#     openai_api_key="9bMmPRH5lWsoWMUZwIMbewihWp29ur4y",
#     openai_api_base="https://api.mistral.ai/v1"
# )

# tools = [tavily_search]

# agent_executor = initialize_agent(
#     tools=tools,
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     handle_parsing_errors=True,
#     verbose=True
# )

# # --- Agent input state ---
# class Agent(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# # --- Node function ---
# def chat_with_llm(state: Agent):
#     input_messages = state["messages"]

#     # Convert messages to a format the agent can understand
#     # Create a conversation context by concatenating previous messages
#     conversation_context = ""
#     for msg in input_messages[:-1]:  # All messages except the last one
#         if hasattr(msg, 'content'):
#             role = "Human" if msg.__class__.__name__ == "HumanMessage" else "Assistant"
#             conversation_context += f"{role}: {msg.content}\n"

#     # Get the current user input
#     current_input = input_messages[-1].content

#     # Combine context with current input
#     if conversation_context:
#         full_input = f"Previous conversation:\n{conversation_context}\nCurrent question: {current_input}"
#     else:
#         full_input = current_input

#     response = agent_executor.run(full_input)
#     return {"messages": [AIMessage(content=response)]}

# # --- Build graph ---
# from langgraph.graph import StateGraph, START, END
# from langgraph.checkpoint.memory import InMemorySaver

# workflow = StateGraph(Agent)

# workflow.add_node("chat_with_llm", chat_with_llm)

# workflow.add_edge(START, "chat_with_llm")
# workflow.add_edge("chat_with_llm", END)

# checkpointer = InMemorySaver()

# graph = workflow.compile(checkpointer=checkpointer)