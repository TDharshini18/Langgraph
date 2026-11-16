# from typing import Annotated,Sequence,TypedDict
# from dotenv  import load_dotenv
# from  langchain_core.messages import BaseMessage,AIMessage,HumanMessage, ToolMessage,SystemMessage
# from langchain_groq import ChatGroq
# from langchain_core.tools  import tool
# from langgraph.graph.message  import add_messages
# from langgraph.graph  import StateGraph,END
# from langgraph.prebuilt  import ToolNode

# load_dotenv()


# documet_content=""  

# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage],add_messages]

# @tool
# def update(content:str)->str:
#     """"Update the document with the provided content."""
#     global documet_content
#     documet_content=content
#     return f"Documet has been updated  {documet_content}"

# @tool
# def save(filename:str)->str:
#     """Save the current documet to a text file and complete the process
#     Args:
#         filename:Name for the text file.
#     """

#     global documnet_content

#     if not filename.endwith(".txt"):
#         filename=filename+".txt"
#     try:
#         with open(filename,"w") as file:
#             file.write(documet_content)
#             print("Documet has been saved")
#             return "Documet has been saved"
#     except Exception as e:
#         return "Error saving document"+ str(e)
    
# tools=[update,save]

# model=ChatGroq(model="openai/gpt-oss-120b").bind_tools(tools)
# def agent(state:AgentState)->AgentState:
#     system_prompt=SystemMessage(content=""" You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
#     - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
#     - If the user wants to save and finish, you need to use the 'save' tool.
#     - Make sure to always show the current document state after modifications.
    
#     The current document content is"""+documet_content)

#     if not state["messages"]:
#         user_input="Ready to update a doc.What would you like to create?"
#         user_message=HumanMessage(content=user_input)

#     else:
#         user_input=input("What would u like me to do with the doc:")
#         print("User:",user_input)
#         user_message=HumanMessage(content=user_input)

#     all_messages=[system_prompt]+list(state['mesasges'])+[user_message]
#     response=model.invoke(all_messages)
#     print("AI:",response.content)
#     if hasattr(response, "tool_calls") and response.tool_calls:
#         print(f"USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

#     return {"messages": list(state["messages"]) + [user_message, response]}

# def should_continue(state)->str:
#     """Determins if the conversation is over or to be continued"""
#     message=state["messages"]
#     if not message:
#         return 'coninue'

#     for m in reversed(message):
#         if (isinstance(m, ToolMessage) and 
#             "saved" in m.content.lower() and
#             "document" in m.content.lower()):
#             return "end" 
#     return "continue"

# def print(message):
#     """Funcrion to print messages in a readable format """
#     if not message:
#         return
#     for message in message[-3:]:
#         if isinstance(message, ToolMessage):
#             print(f"\ TOOL RESULT: {message.content}")



# graph= StateGraph(AgentState)
# graph.add_node("agent",agent)
# graph.add_node("tools",ToolNode(tools))
# graph.set_entry_point("agent")
# graph.add_edge("agent","tools")

# graph.add_contional_edges(
#     "tools",
#     should_continue,
#     {
#         "continue":"agent",
#         "end":END
#     },
    
# )


# app=graph.complie()

# def run_document_agent():
#     print("\n ===== DRAFTER =====")
    
#     state = {"message": []}
    
#     for step in app.stream(state, stream_mode="values"):
#         if "message" in step:
#             print_messages(step["messages"])
    
#     print("\n ===== DRAFTER FINISHED =====")

# if __name__ == "__main__":
#     run_document_agent()

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, ToolMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os
load_dotenv()


document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Tools

@tool
def update(content: str) -> str:
    """Update the document with the provided content."""

    global document_content
    document_content = content

    return f"Document has been updated: {document_content}"

@tool
def save(filename: str) -> str:
    """Save the current document to a text file."""

    global document_content

    if not filename.endswith(".txt"):
        filename += ".txt"

    try:
        print("CURRENT DIRECTORY:", os.getcwd())
        print("DOCUMENT LENGTH:", len(document_content))

        filepath = os.path.abspath(filename)

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(document_content)

        return f"Document saved at: {filepath}"

    except Exception as e:
        return f"Error saving document: {e}"

# @tool
# def save(filename: str) -> str:
#     """Save the current document to a text file and complete the process.
    
#     Args:
#         filename: Name for the text file.
#     """

#     global document_content

#     if not filename.endswith(".txt"):
#         filename = filename + ".txt"

#     try:
#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(document_content)
#             print("Document has been saved")
#             print("Saved at:", os.path.abspath(filename))
#             return "Document has been saved"

#     except Exception as e:
#         return "Error saving document: " + str(e)


tools = [update, save]

model = ChatGroq(model="openai/gpt-oss-120b").bind_tools(tools)


def agent(state: AgentState) -> AgentState:

    system_prompt = SystemMessage(
        content="""You are Drafter, a helpful writing assistant.
        
        - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
        - If the user wants to save and finish, you need to use the 'save' tool.
        - Make sure to always show the current document state after modifications.
        
        The current document content is """ + document_content
    )

    if not state["messages"]:
        user_input = "Ready to update a document. What would you like to create?"
        user_message = HumanMessage(content=user_input)

    else:
        user_input = input("What would you like me to do with the document: ")
        print("User:", user_input)
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state["messages"]) + [user_message]

    response = model.invoke(all_messages)

    print("AI:", response.content)

    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    """Determines if the conversation is over or should be continued."""

    messages = state["messages"]

    if not messages:
        return "continue"

    for m in reversed(messages):
        if (
            isinstance(m, ToolMessage)
            and "saved" in m.content.lower()
            and "document" in m.content.lower()
        ):
            return "end"

    return "continue"


def print_messages(messages):
    """Function to print messages in a readable format."""

    if not messages:
        return

    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\nTOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_edge("agent", "tools")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)

app = graph.compile()


def run_document_agent():

    print("\n===== DRAFTER =====")

    state = {"messages": []}

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])

    print("\n===== DRAFTER FINISHED =====")


if __name__ == "__main__":
    run_document_agent()
