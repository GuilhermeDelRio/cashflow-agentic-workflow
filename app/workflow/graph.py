from typing import Optional
from langgraph.graph import StateGraph, MessagesState
from langchain_core.messages import AIMessage

class AgentState(MessagesState):
    plan: Optional[str]


def planner_node(state: AgentState):
    messages = state.get("messages", [])

    if not messages:
        return {}

    user_text = messages[-1].content
    plan = f"Plano para: {user_text}"

    return {
        "messages": [AIMessage(content=plan)],
        "plan": plan
    }


graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.set_entry_point("planner")
graph.set_finish_point("planner")

app = graph.compile()
