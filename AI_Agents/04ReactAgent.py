from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.messages  import ToolMessage
from  langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]


#tools
@tool  
def add(a:int,b:int):
    """This is  an addition function that adds two  numbers"""
    return a+b

tools=[add]
#gives  models  access to  tools
model=ChatGroq(model="openai/gpt-oss-120b").bind_tools(tools)

def model_call(state):
    system_prompt=SystemMessage(content="You are my  ai assistance,Answere the qns to the best of your ability")
    
    #response=model.invoke(["You are my  ai assistance,Answere the qns to the best of your ability"])
    response=model.invoke([system_prompt]+state['messages'])
    return {"messages":[response]}


def should_continue(state: AgentState):
    last_message = state['messages'][-1]
    if not last_message.tool_calls:
        return "end"
    return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", ToolNode(tools=tools))

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)
graph.add_edge("tools", "our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "Use the add tool to add 342 + 90177.")]}
print_stream(app.stream(inputs, stream_mode="values"))
