# Cashflow Agentic Workflow

An intelligent cashflow management system powered by LLM-based agents. This project uses LangGraph to create specialized AI agents that help users manage their finances through natural language conversations.

## What is this?

This is an **agentic workflow system** that allows users to manage their cashflow (expenses, income, budgets) by simply chatting with an AI assistant. Instead of clicking through forms and menus, you can say things like:

- "Add a $50 expense for groceries"
- "Show me all my expenses this month"
- "Update my Netflix subscription to $15.99"
- "Delete expense #42"

The system uses **LangGraph** to orchestrate multiple specialized AI agents, each responsible for a specific domain (expenses, income, etc.). A router agent analyzes your request and routes it to the appropriate specialist.

## Architecture

### Multi-Agent System

The project follows a **router/orchestrator pattern** with specialized agents:

```
User Request
     ↓
Router Agent (Intent Classification)
     ↓
├─→ Expense Agent (manage expenses)
├─→ Income Agent (track income) [planned]
├─→ Budget Agent (budget planning) [planned]
└─→ General Agent (fallback)
```

Each agent is built with **LangGraph** and has:
- **LLM-powered reasoning** (Groq/OpenAI)
- **Specialized tools** (create, read, update, delete operations)
- **Domain-specific prompts** (optimized for their task)
- **Type-safe schemas** (Pydantic validation)

### Technology Stack

- **LangGraph**: Agentic workflow orchestration
- **LangChain**: LLM integration and tool calling
- **Groq/OpenAI**: LLM providers (Llama 3.3, GPT-4o-mini)
- **Python 3.13**: Core language
- **uv**: Fast Python package manager
- **Telegram Bot API**: Conversational interface
- **FastAPI Backend**: Separate API service ([cashflow-backend](https://github.com/GuilhermeDelRio/cashflow-backend))

## Features

### Current Features
- Natural language expense management
- Telegram bot interface
- Multi-agent routing system
- Tool-calling with type safety
- Support for multiple LLM providers (Groq, OpenAI)

### Planned Features
- Income tracking agent
- Budget planning agent
- Financial reports and analytics
- Recurring expense detection
- Multi-currency support

## Getting Started

### Prerequisites

- Python 3.13+
- uv (recommended) or pip
- API keys for Groq and/or OpenAI
- (Optional) Telegram bot token

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cashflow-agentic-workflow.git
cd cashflow-agentic-workflow
```

2. Install dependencies:
```bash
make install
# or: uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `GROQ_API_KEY` and/or `OPENAI_API_KEY` (at least one required)
- `TELEGRAM_BOT_TOKEN` (optional, for Telegram bot)
- `OPENAI_BASE_URL` (optional, for custom OpenAI endpoints)

### Running the Application

**Telegram Bot** (recommended):
```bash
make telegram
# or: uv run python telegram_main.py
```

**LangGraph Development UI** (for testing workflows):
```bash
make dev
# or: uv run langgraph dev
```

**CLI** (basic):
```bash
make run
# or: uv run python main.py
```

## Usage Examples

### Via Telegram Bot

Once the bot is running, message it with natural language:

```
You: Add an expense of $120 for electricity bill
Bot: Expense created successfully! I've added a $120.00 expense for electricity bill.

You: Show my expenses
Bot: Here are your expenses:
     1. Electricity bill - $120.00 (2026-03-28)
     2. Groceries - $85.50 (2026-03-27)
     ...

You: Update expense 1 to $125
Bot: Expense updated! The electricity bill is now $125.00.
```

### LangGraph Studio

For visual workflow debugging:
1. Run `make dev`
2. Open the provided URL in your browser
3. Select the "router" graph
4. Input messages and watch the agent routing in real-time

## Project Structure

```
app/
├── agents/
│   ├── router/              # Main orchestrator
│   │   ├── graph.py         # Routing logic
│   │   └── prompts/         # Intent classification prompts
│   ├── expense/             # Expense management agent
│   │   ├── graph.py         # LangGraph workflow
│   │   ├── tools.py         # Expense CRUD tools
│   │   ├── schemas.py       # Pydantic models
│   │   └── prompts/         # Agent system prompts
│   └── shared/              # Shared utilities
│       └── base.py          # LLM helpers, prompt loaders
├── config/
│   └── settings.py          # Configuration management
└── integrations/
    └── telegram/            # Telegram bot integration
        ├── bot.py
        └── handlers.py
```

## Backend API

The backend API is developed separately and handles data persistence, authentication, and business logic:

**Repository**: [cashflow-backend](https://github.com/GuilhermeDelRio/cashflow-backend)

The agentic workflow system communicates with the backend via REST API calls defined in the agent tools.

## Development

### Available Commands

```bash
make help          # Show all available commands
make install       # Install dependencies
make test          # Run tests
make lint          # Run linter
make format        # Format code
make type-check    # Run type checker
make all           # Run all checks
make clean         # Clean cache files
```

### Adding a New Agent

1. Create agent directory: `app/agents/{agent_name}/`
2. Define schemas in `schemas.py`
3. Implement tools in `tools.py` with `@tool` decorator
4. Create agent prompt in `prompts/agent.md`
5. Build LangGraph workflow in `graph.py`
6. Register in `langgraph.json`
7. Integrate with router in `app/agents/router/graph.py`

See `CLAUDE.md` for detailed instructions.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run tests and linting before committing
4. Submit a pull request


## Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [Groq](https://groq.com/) - Fast LLM inference
- [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram integration