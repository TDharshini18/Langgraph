from typing import Annotated,Sequence,TypedDict
from dotenv  import load_dotenv
from  langchain_core.messages import BaseMessage,AIMessage,HumanMessage, ToolMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools  import tool
from langgraph.graph.message  import add_messages
from langgraph.graph  import StateGraph,END
from langgraph.prebuilt  import ToolNode

load_dotenv()


documet_content=""  

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def update(content:str)->str:
    """"Update the document with the provided content."""
    global documet_content
    documet_content=content
    return f"Documet has been updated  {documet_content}"

@tool
def save(filename:str)->str:
    global  documet_content
    documet_content=content