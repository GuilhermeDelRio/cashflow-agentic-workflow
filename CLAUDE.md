# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph-based agentic workflow system for managing cashflow and expenses. The application uses LLM-powered agents to handle user requests through structured, tool-calling workflows.

## Development Commands

**Quick Start:** Use `make help` to see all available commands.

**Note:** This project uses `uv` for dependency management. All commands in the Makefile use `uv run` to execute tools in the virtual environment.

### Environment Setup
```bash
# Install dependencies using uv
make install
# or: uv sync

# Install dev dependencies
make install-dev
# or: uv sync --group dev

# Sync all dependencies
make sync
```

### Running the Application
```bash
# Run the main application
make run
# or: uv run python main.py

# Test LangGraph workflows with UI
make dev
# or: uv run langgraph dev

# Run Telegram bot
make telegram
# or: uv run python telegram_main.py
```

### Testing and Code Quality
```bash
# Run tests
make test
# or: uv run pytest

# Run linter
make lint
# or: uv run ruff check .

# Format code
make format
# or: uv run ruff format .

# Run type checker
make type-check
# or: uv run mypy .

# Run all checks (format, lint, type-check, test)
make all
```

### Maintenance
```bash
# Clean cache files and __pycache__
make clean
```

## Architecture

### Domain-Driven Feature Module Structure
The project follows a **domain-driven architecture** where each agent is a self-contained feature module:

```
app/
├── agents/
│   ├── router/               # Router/Orchestrator - main entry point
│   │   ├── graph.py          # Routing logic and subgraph invocation
│   │   └── prompts/
│   │       └── agent.md      # Intent classification prompt
│   ├── expense/              # Expense domain - specialized agent
│   │   ├── graph.py          # LangGraph workflow definition
│   │   ├── tools.py          # Domain-specific tools
│   │   ├── schemas.py        # Pydantic models
│   │   └── prompts/
│   │       └── agent.md      # System prompt
│   ├── income/               # Income domain (future)
│   └── shared/               # Shared utilities across agents
│       └── base.py           # Base workflow helpers
├── config/                   # Global configuration
│   └── settings.py
└── integrations/             # External integrations
    └── telegram/             # Telegram bot integration
        ├── bot.py            # Bot initialization
        └── handlers.py       # Message handlers
```

**Benefits:**
- All code for one feature (expense) lives in one place
- Router orchestrates requests to specialized agents
- Easy to add new agents (income, budget, reports) without affecting existing ones
- Clear separation of concerns between domains
- Shared utilities prevent duplication

### LangGraph Workflow Architecture
The project uses LangGraph's tool-calling pattern with direct LLM integration. Agents are registered in `langgraph.json`:
- **router**: Main orchestrator that routes to specialized agents (`./app/agents/router/graph.py:app`)
- **expense_agent**: Expense management workflow (`./app/agents/expense/graph.py:app`)

Key LangGraph concepts used:
- **StateGraph**: Defines node-based execution flows
- **MessagesState**: Manages conversation history and message passing between nodes
- **ToolNode**: Executes LangChain tools called by the LLM
- **Conditional edges**: Routes between agent and tool nodes based on LLM response
- **Subgraph invocation**: Router invokes specialized agent graphs

### Router/Orchestrator Pattern
The **router agent** serves as the main application entry point and orchestrates requests to specialized agents:

**Flow:**
1. **User Request** → Router receives the message
2. **Intent Classification** → Router LLM classifies intent (expense, income, general, etc.)
3. **Conditional Routing** → Routes to appropriate specialized agent based on intent
4. **Specialized Agent** → Invokes the corresponding agent subgraph (e.g., expense_app)
5. **Response** → Returns results to user

**Key Components** (app/agents/router/graph.py):
- `router_node`: Classifies user intent using LLM
- `route_to_agent`: Conditional function that routes based on intent
- `expense_agent_node`: Invokes expense agent subgraph
- `general_agent_node`: Handles fallback/general queries
- `RouterState`: Extended state with `intent` field

**Example Router Implementation:**
```python
from app.agents.expense.graph import app as expense_app

def expense_agent_node(state: MessagesState) -> dict:
    """Invokes the expense agent subgraph"""
    messages = state["messages"]
    result = expense_app.invoke({"messages": messages})
    return {"messages": result["messages"]}

graph.add_conditional_edges("router", route_to_agent, {
    "expense_agent": "expense_agent",
    "general_agent": "general_agent"
})
```

### Specialized Agent Pattern
Each specialized agent follows this pattern:
1. **Agent Node**: LLM with bound tools analyzes messages and decides which tool(s) to call
2. **Conditional Edge**: Routes to tools if LLM made tool calls, otherwise ends
3. **Tool Node**: Executes the called tools
4. **Edge back**: Returns tool results to agent node for synthesis

Example workflow structure (app/agents/expense/graph.py):
```python
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode
from ..shared.base import create_groq_llm, load_agent_prompt, create_agent_node, should_continue
from .tools import create_expense, list_expenses, update_expense, delete_expense

tools = [create_expense, list_expenses, update_expense, delete_expense]
llm = create_groq_llm()
llm_with_tools = llm.bind_tools(tools)
prompt_content = load_agent_prompt("expense")
expense_agent_node = create_agent_node(llm_with_tools, prompt_content)

graph = StateGraph(MessagesState)
graph.add_node("expense_agent", expense_agent_node)  # Use descriptive node names
graph.add_node("expense_tools", ToolNode(tools))
graph.set_entry_point("expense_agent")
graph.add_conditional_edges("expense_agent", should_continue, {"tools": "expense_tools", END: END})
graph.add_edge("expense_tools", "expense_agent")
app = graph.compile()
```

**IMPORTANT - Node Naming Convention:**
- Always use descriptive node names that include the domain: `expense_agent`, `income_agent`
- Never use generic names like `agent` or `tools`
- This makes debugging easier and prevents confusion when working with multiple agents

### LLM Integration
The project uses direct LangChain LLM integrations with helper functions in `app/agents/shared/base.py`:
- **create_groq_llm()**: Creates ChatGroq instances (default: `llama-3.3-70b-versatile`)
- **create_openai_llm()**: Creates ChatOpenAI instances (default: `gpt-4o-mini`)

LLMs are instantiated using these helpers and bound to tools using `.bind_tools(tools)`.

**Available Models:**
- Groq: `llama-3.3-70b-versatile`, `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`
- OpenAI: All models supported by `langchain-openai`

**Shared Utilities** (`app/agents/shared/base.py`):
- `create_groq_llm(model, temperature)`: Instantiate Groq LLM
- `create_openai_llm(model, temperature)`: Instantiate OpenAI LLM
- `load_agent_prompt(agent_name, prompt_filename)`: Load agent prompts
- `should_continue(state)`: Standard conditional routing function
- `create_agent_node(llm_with_tools, prompt_content)`: Create agent node function

### Configuration
Settings are managed in `app/config/settings.py` using Pydantic:
- Environment variables loaded via `python-dotenv`
- **Required**: At least one of `OPENAI_API_KEY` or `GROQ_API_KEY`
- **Optional**: `OPENAI_BASE_URL` for custom OpenAI endpoints, `TELEGRAM_BOT_TOKEN` for Telegram integration
- Validation ensures at least one provider is configured

### Prompt Management
Prompts are stored within each agent's feature module:
- **load_agent_prompt(agent_name)** (`app/agents/shared/base.py`): Loads prompts from agent's prompts directory
- Prompts are injected as SystemMessage at the start of conversations
- Example: `load_agent_prompt("expense")` loads `app/agents/expense/prompts/agent.md`

### Schemas and Tools (Example: Expense Agent)
**Schemas** (`app/agents/expense/schemas.py`):
- `ExpenseData`: Pydantic model for expense records with validation
- `ExpenseUpdate`: Pydantic model for expense updates
- `RecurrenceType`: Enum for recurrence types (monthly, yearly)
- `ExpenseAgentAction`: Action types for agent decisions

**Tools** (`app/agents/expense/tools.py`):
- LangChain tools decorated with `@tool`
- **Use Pydantic models for type safety** (ExpenseData, ExpenseUpdate)
- Currently mocked (API calls commented out)
- Available tools:
  - `create_expense(expense: ExpenseData)`: Creates expense using validated model
  - `list_expenses()`: Lists all expenses
  - `update_expense(expense_id: int, updates: ExpenseUpdate)`: Updates with validated model
  - `delete_expense(expense_id: int)`: Deletes expense by ID

## Key Patterns

### Adding a New Agent (Feature Module)
1. **Create agent directory**: `app/agents/{agent_name}/`
2. **Create schemas.py**: Define Pydantic models for your domain
3. **Create tools.py**:
   - Import domain schemas
   - Define tools using `@tool` decorator
   - Use Pydantic models for parameters (type safety)
   - Add comprehensive docstrings
4. **Create prompts/agent.md**: System prompt with Role, Task, Instructions, Examples
5. **Create graph.py** (using absolute imports):
   ```python
   from langgraph.graph import StateGraph, MessagesState, END
   from langgraph.prebuilt import ToolNode
   from app.agents.shared.base import create_groq_llm, load_agent_prompt, create_agent_node, should_continue
   from app.agents.{agent_name}.tools import tool1, tool2, tool3

   tools = [tool1, tool2, tool3]
   llm = create_groq_llm()  # or create_openai_llm()
   llm_with_tools = llm.bind_tools(tools)
   prompt_content = load_agent_prompt("{agent_name}")
   agent_node = create_agent_node(llm_with_tools, prompt_content)

   graph = StateGraph(MessagesState)
   graph.add_node("{agent_name}_agent", agent_node)  # Use domain-specific name
   graph.add_node("{agent_name}_tools", ToolNode(tools))
   graph.set_entry_point("{agent_name}_agent")
   graph.add_conditional_edges("{agent_name}_agent", should_continue, {"tools": "{agent_name}_tools", END: END})
   graph.add_edge("{agent_name}_tools", "{agent_name}_agent")
   app = graph.compile()
   ```
6. **Create __init__.py**: Export the app
7. **Register in langgraph.json**: Add entry under "graphs"

**Naming Best Practices:**
- Node names MUST include the domain name (e.g., `expense_agent`, `income_agent`, `budget_tools`)
- Never use generic names like `agent` or `tools`
- This prevents confusion and makes LangGraph Studio visualization clearer

**Import Pattern - CRITICAL:**
- **Always use absolute imports** in graph files, NOT relative imports
- LangGraph loads files directly via paths, so relative imports fail
- Example:
  ```python
  # ❌ WRONG - Relative import (will fail with LangGraph)
  from ..shared.base import create_groq_llm
  from .tools import create_expense

  # ✅ CORRECT - Absolute import
  from app.agents.shared.base import create_groq_llm
  from app.agents.expense.tools import create_expense
  ```

### Adding Tools to Existing Agent
1. Define Pydantic model in `schemas.py` (if needed)
2. Add tool function in `tools.py` with `@tool` decorator
3. Use Pydantic models for parameters
4. Import and add to tools list in `graph.py`
5. Update prompt in `prompts/agent.md` to describe new tool

### Changing LLM Models
Modify the graph.py file:
```python
# Use Groq
llm = create_groq_llm(model="llama-3.1-70b-versatile", temperature=0)

# Use OpenAI
llm = create_openai_llm(model="gpt-4o", temperature=0)
```

### Using Shared Utilities
Import from `app/agents/shared/base.py`:
- `create_groq_llm()` / `create_openai_llm()`: Initialize LLMs
- `load_agent_prompt(agent_name)`: Load prompts
- `should_continue()`: Standard routing logic
- `create_agent_node()`: Create agent node with prompt injection

### Integrating New Agent with Router
When you add a new specialized agent (e.g., income), integrate it with the router:

1. **Update router prompt** (`app/agents/router/prompts/agent.md`):
   ```markdown
   # Available Agents
   - **expense**: Handles expense management
   - **income**: Handles income tracking
   - **general**: Handles general questions

   # Classification Rules
   - If user mentions income, salary, revenue → **income**
   ```

2. **Import new agent in router** (`app/agents/router/graph.py`):
   ```python
   from app.agents.expense.graph import app as expense_app
   from app.agents.income.graph import app as income_app  # Add this
   ```

3. **Create agent node**:
   ```python
   def income_agent_node(state: MessagesState) -> dict:
       """Invokes the income agent subgraph"""
       messages = state["messages"]
       user_messages = [msg for msg in messages if not msg.content.startswith("[Routing")]
       result = income_app.invoke({"messages": user_messages})
       return {"messages": result["messages"]}
   ```

4. **Add to graph**:
   ```python
   graph.add_node("income_agent", income_agent_node)
   ```

5. **Update routing logic**:
   ```python
   def route_to_agent(state: MessagesState) -> str:
       intent = state.get("intent", "general")
       if intent == "expense":
           return "expense_agent"
       elif intent == "income":
           return "income_agent"
       else:
           return "general_agent"

   graph.add_conditional_edges("router", route_to_agent, {
       "expense_agent": "expense_agent",
       "income_agent": "income_agent",
       "general_agent": "general_agent"
   })

   graph.add_edge("income_agent", END)
   ```

6. **Register in langgraph.json**:
   ```json
   {
     "graphs": {
       "router": "./app/agents/router/graph.py:app",
       "expense_agent": "./app/agents/expense/graph.py:app",
       "income_agent": "./app/agents/income/graph.py:app"
     }
   }
   ```

## Telegram Bot Integration

The project includes a Telegram bot integration that provides a conversational interface to the agentic workflow system.

### Architecture
The Telegram integration is located in `app/integrations/telegram/`:
- **bot.py**: Initializes the Telegram bot application and registers handlers
- **handlers.py**: Implements message handling logic that invokes the router graph

### How It Works
1. User sends a message to the Telegram bot
2. `message_handler` receives the message and invokes the router graph
3. Router classifies intent and routes to the appropriate specialized agent (expense, income, etc.)
4. Agent processes the request using LLM + tools
5. Response is sent back to the user via Telegram

### Setup
1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram
2. Get your bot token from BotFather
3. Add `TELEGRAM_BOT_TOKEN=your_token_here` to `.env`
4. Run `make telegram` or `uv run python telegram_main.py`

### Available Commands
- `/start` - Welcome message and bot introduction
- `/help` - Show help with available features
- Any text message - Processed through the router agent workflow

### Key Features
- Natural language processing via LangGraph workflows
- Automatic intent classification and routing
- Full access to all agent capabilities (expense, income, etc.)
- Error handling and user feedback
- Typing indicators during processing

## Current State

The project is in active development with:
- Working expense management workflow with tool-calling
- Telegram bot integration for conversational interface
- Basic CLI interface in `main.py` (simple input loop, not connected to workflows)
- LangGraph test UI available via `langgraph dev`
- Mocked API calls in tools (ready for backend integration)
- No comments in code unless EXTREMELY NECESSARY
