from langgraph.graph import MessagesState, END
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from pathlib import Path
from typing import Callable


def load_agent_prompt(agent_name: str, prompt_filename: str = "agent.md") -> str:
    """
    Load a prompt template from an agent's prompts directory.

    Args:
        agent_name: Name of the agent (e.g., "expense")
        prompt_filename: Name of the prompt file (default: "agent.md")

    Returns:
        The content of the prompt file as a string
    """
    agents_dir = Path(__file__).parent.parent
    prompt_path = agents_dir / agent_name / "prompts" / prompt_filename
    return prompt_path.read_text()


def create_groq_llm(
    model: str = "llama-3.3-70b-versatile", temperature: float = 0
) -> ChatGroq:
    """
    Create a ChatGroq LLM instance.

    Args:
        model: Groq model name
        temperature: Model temperature (0-1)

    Returns:
        Configured ChatGroq instance
    """
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=settings.groq_api_key,
    )


def create_openai_llm(model: str = "gpt-4o-mini", temperature: float = 0) -> ChatOpenAI:
    """
    Create a ChatOpenAI LLM instance.

    Args:
        model: OpenAI model name
        temperature: Model temperature (0-1)

    Returns:
        Configured ChatOpenAI instance
    """
    kwargs = {
        "model": model,
        "temperature": temperature,
        "api_key": settings.openai_api_key,
    }
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url
    return ChatOpenAI(**kwargs)


def should_continue(state: MessagesState) -> str:
    """
    Standard conditional function to determine whether to continue to tools or end.

    Args:
        state: Current MessagesState

    Returns:
        "tools" if last message has tool calls, END otherwise
    """
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


def create_agent_node(llm_with_tools, prompt_content: str) -> Callable:
    """
    Create a standard agent node function.

    Args:
        llm_with_tools: LLM instance with tools bound
        prompt_content: System prompt content

    Returns:
        Agent node function that can be used in StateGraph
    """

    def agent_node(state: MessagesState) -> dict:
        messages = state["messages"]

        if not any(isinstance(msg, SystemMessage) for msg in messages):
            system_msg = SystemMessage(content=prompt_content)
            messages = [system_msg] + messages

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    return agent_node
