from typing import TypedDict,Union

from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
class AgentState(TypedDict):
    messages: list[Union[HumanMessage,AIMessage]]

llm=ChatOpenAI(model="gpt-4o")
def process(state):
    """This node will solve req u input"""
    response=llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))