from typing import TypedDict,Union

from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: list[Union[HumanMessage,AIMessage]]

llm=ChatGroq(model="openai/gpt-oss-120b")
def process(state):
    """This node will solve req u input"""
    response=llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print("AI: ", response.content)
    return state

graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

# conversation history is kept between turns so the bot remembers
conversation_history=[]

user_input=input("Enter: ")
while user_input!="exit":
    conversation_history.append(HumanMessage(content=user_input))
    result=agent.invoke({"messages":conversation_history})
    conversation_history=result["messages"]
    user_input=input("Enter: ")

# save the conversation to a file
with open("logging.txt","w",encoding="utf-8") as file:
    file.write("Your Conversation Log:\n")
    for message in conversation_history:
        if isinstance(message,HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message,AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")
print("Conversation saved to logging.txt")
