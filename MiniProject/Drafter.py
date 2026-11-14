from typing import Annotated,Sequence,TypedDict
from dotenv  import load_dotenv
from  langchain_core.messages import BaseMessage,AIMessage,HumanMessage, ToolMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools  import ToolsRenderer
from langgraph.graph.message  import add_messages
from langgraph.graph  import StateGraph,END
from langgraph.prebuilt  import ToolNode

load_dotenv()


documet_content=""
