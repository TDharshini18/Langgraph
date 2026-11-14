#integrate llm into graphs
from typing import TypedDict
from langgraph.graph import StateGraph , START,END
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()

class AgentState(TypedDict):
    messages: list[HumanMessage]

llm=ChatGroq(model="openai/gpt-oss-120b")

def process(state:AgentState) -> AgentState:
    response=llm.invoke(state["messages"])
    print("AI: ", response.content)
    return state
graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,'process')
graph.add_edge('process',END)
agent=graph.compile()
user_input=input("Enter query: ")
agent.invoke({"messages":[HumanMessage(content=user_input)]})
