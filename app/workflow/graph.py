from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import AIMessage


def entry_node(state: MessagesState) -> dict:
    messages = state.get("messages", [])

    if not messages:
        return {"messages": [AIMessage(content="No input received.")]}

    user_message = messages[-1].content
    
    response = f"Received: {user_message}"

    return {"messages": [AIMessage(content=response)]}


graph = StateGraph(MessagesState)
graph.add_node("entry", entry_node)
graph.set_entry_point("entry")
graph.set_finish_point("entry")

app = graph.compile()