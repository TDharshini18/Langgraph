from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.messages  import ToolMessage
from  langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
class AgentState(TypedDict):
    message:  Annotated[Sequence[BaseMessage],add_messages]


#tools
@tool  
def add(a:int,b:int):
    """This is  an addition function that adds two  numbers"""
    return a+b

tools=[add]
#gives  models  access to  tools
model=ChatOpenAI(model="gpt-4o").bind_tools(tools)

def model_call(state):
    system_prompt=SystemMessage(content="You are my  ai assistance,Answere the qns to the best of your ability")
    
    #response=model.invoke(["You are my  ai assistance,Answere the qns to the best of your ability"])
    response=model.invoke([system_prompt]+state['message'])
    return {"message":[response]}
