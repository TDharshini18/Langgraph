from typing import TypedDict
from langgraph.graph import StateGraph

class Agent(TypedDict):
    list_no: list[int]
    name: str
    result: str

def sum_values(state:Agent) ->Agent:
    """Adds the given no's sum"""
    print(state)
    state["result"]="Hi there "+state["name"],"! Your sum= "+ str(sum(state["list_no"]))
    print(state)
    return state

graph=StateGraph(Agent)
graph.add_node("sum_values",sum_values)
graph.set_entry_point("sum_values")
graph.set_finish_point("sum_values")
app=graph.compile()
ans=app.invoke({"list_no":[10,20,30,40],"name":"bob"})
print(ans["result"])