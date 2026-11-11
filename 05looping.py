from typing import List, TypedDict
import random

from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int


def greeting_node(state: AgentState) -> AgentState:
    """Greets the person and resets the counter."""
    state["name"] = "Hi there, " + state["name"]
    state["counter"] = 0
    return state


def random_node(state: AgentState) -> AgentState:
    """Adds one random number from 0 to 10 and increments the counter."""
    state["number"].append(random.randint(0, 10))
    state["counter"] += 1
    return state


def should_continue(state: AgentState) -> str:
    """Decides whether to loop back or exit."""
    if state["counter"] < 5:
        print("ENTERING LOOP", state["counter"])
        return "loop"
    return "exit"


graph = StateGraph(AgentState)

graph.add_node("greeting", greeting_node)
graph.add_node("random", random_node)

graph.add_edge("greeting", "random")

graph.add_conditional_edges(
    "random",
    should_continue,
    {
        "loop": "random",
        "exit": END,
    },
)

graph.set_entry_point("greeting")

app = graph.compile()

result = app.invoke({"name": "dharshini", "number": [], "counter": -100})
print(result)