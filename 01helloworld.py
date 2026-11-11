from langgraph.graph import StateGraph
from typing import TypedDict
class Agent(TypedDict):
    message:str

def greeting(state:Agent) -> Agent:
    """A node that greets message"""
    state['message']="Hey "+state['message']+ " How are you?"

    return state

graph=StateGraph(Agent)
graph.add_node("greeter",greeting)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")
app=graph.compile()
result=app.invoke({"message":"bob"})
print(result['message'])
