from langchain_core.messages import HumanMessage, AIMessage
from app.workflow.graph import app, entry_node


class TestEntryNode:
    def test_entry_node_with_message(self):
        state = {
            "messages": [HumanMessage(content="Hello world")]
        }

        result = entry_node(state)

        assert "messages" in result
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)
        assert "Hello world" in result["messages"][0].content

    def test_entry_node_empty_messages(self):
        state = {"messages": []}

        result = entry_node(state)

        assert "messages" in result
        assert result["messages"][0].content == "No input received."

    def test_entry_node_no_messages_key(self):
        state = {}

        result = entry_node(state)

        assert "messages" in result
        assert result["messages"][0].content == "No input received."


class TestGraph:
    def test_graph_invoke_success(self):
        result = app.invoke({
            "messages": [HumanMessage(content="Test message")]
        })

        assert "messages" in result
        assert len(result["messages"]) > 0
        assert isinstance(result["messages"][-1], AIMessage)

    def test_graph_invoke_empty(self):
        result = app.invoke({"messages": []})

        assert "messages" in result
        assert result["messages"][-1].content == "No input received."

    def test_graph_preserves_message_history(self):
        result = app.invoke({
            "messages": [
                HumanMessage(content="First"),
                AIMessage(content="Response"),
                HumanMessage(content="Second")
            ]
        })

        assert len(result["messages"]) >= 3
