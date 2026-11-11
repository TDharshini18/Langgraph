from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    number1:int
    number2: int
    operation:str
    ans: int

def adder(state:AgentState)->AgentState:
    """This node adds 2 numbers"""
    state["ans"]=state["number1"]+state["number2"]
    return state

def subtractor(state:AgentState)->AgentState:
    """This node subtracts 2 numbers"""
    state["ans"]=  state["number1"]-state["number2"]
    return state

def decide_operation(state:AgentState)->str:
    """This node decided which operation to perform"""
    if state["operation"]=="+":
        return "Addition Operation"
    else:
        return "Subtration Operation"
graph=StateGraph(AgentState)
graph.add_node("add_node",adder)
graph.add_node("sub_node",subtractor)
graph.add_node("op",lambda state:state)

graph.set_entry_point("op")
graph.add_conditional_edges(
    "op",
    decide_operation,
    {
        "Addition Operation": "add_node",
        "Subtration Operation": "sub_node",
    }
)


graph.set_finish_point("add_node")
graph.set_finish_point("sub_node")    
    
app = graph.compile()

result = app.invoke({"number1": 10, "number2": 5, "operation": "+"})
print(result["ans"])