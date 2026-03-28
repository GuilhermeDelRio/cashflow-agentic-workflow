from langgraph.graph import StateGraph, MessagesState, END
from langchain_core.messages import AIMessage, SystemMessage
from app.agents.shared.base import create_groq_llm, load_agent_prompt
from app.agents.expense.graph import app as expense_app


def router_node(state: MessagesState) -> dict:
    """
    Router node that classifies user intent and stores it in state.
    """
    messages = state["messages"]

    if not any(isinstance(msg, SystemMessage) for msg in messages):
        prompt_content = load_agent_prompt("router")
        system_msg = SystemMessage(content=prompt_content)
        messages = [system_msg] + messages

    llm = create_groq_llm(temperature=0)
    response = llm.invoke(messages)

    intent = response.content.strip().lower()

    return {
        "messages": [AIMessage(content=f"[Routing to {intent} agent]")],
        "intent": intent,
    }


def route_to_agent(state: MessagesState) -> str:
    """
    Conditional routing based on classified intent.
    """
    intent = state.get("intent", "general")

    if intent == "expense":
        return "expense_agent"
    else:
        return "general_agent"


def expense_agent_node(state: MessagesState) -> dict:
    """
    Invokes the expense agent subgraph.
    """
    messages = state["messages"]
    user_messages = [msg for msg in messages if not msg.content.startswith("[Routing")]

    result = expense_app.invoke({"messages": user_messages})

    return {"messages": result["messages"]}


def general_agent_node(state: MessagesState) -> dict:
    """
    Handles general queries, greetings, and fallback responses.
    """
    response = AIMessage(
        content="Hello! I can help you manage your expenses. Try saying 'create an expense' or 'show my expenses'."
    )

    return {"messages": [response]}


class RouterState(MessagesState):
    intent: str = ""


graph = StateGraph(RouterState)
graph.add_node("router", router_node)
graph.add_node("expense_agent", expense_agent_node)
graph.add_node("general_agent", general_agent_node)

graph.set_entry_point("router")
graph.add_conditional_edges(
    "router",
    route_to_agent,
    {"expense_agent": "expense_agent", "general_agent": "general_agent"},
)
graph.add_edge("expense_agent", END)
graph.add_edge("general_agent", END)

app = graph.compile()
