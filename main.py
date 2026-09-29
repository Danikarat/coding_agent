from langchain_core.tools import tool
from langgraph.graph  import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import ToolMessage

# state shared across all graphs
class AgentState(TypedDict):
    messages : Annotated[list, add_messages]
    

# defining a tool 
@tool
def get_weather(city : str)->str:
    """Get the weather for a city"""
    return f"it'ssunny in {city}"

tools =[get_weather]

model = ChatAnthropic(model="claude-sonnet-4-6").bind_tools(tools)



# call node
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# tool node (manual approach)
def tool_node(state : AgentState):
    last_messsage = state["message"][-1]
    results = []
    