from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from app.agents.shared.base import (
    create_groq_llm,
    load_agent_prompt,
    create_agent_node,
    should_continue,
)
from app.agents.expense.tools import create_expense, list_expenses, update_expense, delete_expense

tools = [create_expense, list_expenses, update_expense, delete_expense]

llm = create_groq_llm()
llm_with_tools = llm.bind_tools(tools)

prompt_content = load_agent_prompt("expense")
expense_agent_node = create_agent_node(llm_with_tools, prompt_content)

graph = StateGraph(MessagesState)
graph.add_node("expense_agent", expense_agent_node)
graph.add_node("expense_tools", ToolNode(tools))

graph.set_entry_point("expense_agent")
graph.add_conditional_edges(
    "expense_agent", should_continue, {"tools": "expense_tools", END: END}
)
graph.add_edge("expense_tools", "expense_agent")

app = graph.compile()
