from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: int
    final: str

def first_node(state:AgentState)->AgentState:
    """This is the first node in the sequence"""

    state["final"]="Hi" + state["name"]
    return state
def second_node(state:AgentState)->AgentState:
    """This is the second in the sequence"""
    state["final"]=state["final"]+ "You are" +str(state["age"])
    return state
graph=StateGraph(AgentState)
graph.add_node("first",first_node)
graph.add_node("second",second_node)
graph.add_edge("first","second")
graph.set_entry_point("first")
graph.set_finish_point("second")
app=graph.compile()
result=app.invoke({"name":"bob","age":20})
print(result["final"])
