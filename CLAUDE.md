# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph-based agentic workflow system for managing cashflow and expenses. The application uses LLM-powered agents to route and handle user requests through structured workflows.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv
uv sync

# Install dev dependencies
uv sync --group dev
```

### Running the Application
```bash
# Run the main application
python main.py

# Test LangGraph workflows with UI
langgraph dev
```

### Testing and Code Quality
```bash
# Run tests
pytest

# Run linter
ruff check .

# Run type checker
mypy .
```

## Architecture

### LLM Abstraction Layer
The codebase implements a provider-agnostic LLM system:

- **LLMFactory** (`app/llm/llm_factory.py`): Creates provider-specific clients
- **LLMClient** (`app/llm/llm_client.py`): Abstract base class defining the interface
- **Provider implementations** (`app/llm/providers/`): Concrete implementations (OpenAI, Groq, Ollama)
- **MODEL_REGISTRY** (`app/llm/registry.py`): Maps model names to providers
- **LLMConfig** (`app/llm/llm_config.py`): Configuration for LLM calls

**Supported Providers:**
- **OpenAI**: GPT models via `langchain-openai`
- **Groq**: Fast inference for Llama, Mixtral, and Gemma models via `langchain-groq`
- **Ollama**: Local model serving (partial implementation)

**Available Models:**
- OpenAI: `gpt-4o-mini`, `gpt-4.1`
- Groq: `llama-3.3-70b-versatile`, `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`
- Ollama: `llama3`

To use an LLM: BaseAgent inherits this pattern and calls `self.call_llm(prompt, config)`, which automatically routes to the correct provider based on the model specified in the config.

### Agent Architecture
All agents inherit from `BaseAgent` (`app/agents/base_agent.py`), which provides:
- Access to LLMFactory for making LLM calls
- `call_llm()` method that handles provider routing automatically

Current agents:
- **RouterAgent**: Routes requests to appropriate specialized agents
- **ExpenseAgent**: Handles expense management operations (CREATE, READ, UPDATE, DELETE)

### LangGraph Workflows
Workflows are defined in `app/workflow/` and registered in `langgraph.json`:
- **react_agent**: Basic workflow (`./app/workflow/graph.py:app`)
- **expense_agent**: Expense management workflow (`./app/workflow/expense_workflow.py:app`)

LangGraph workflows use:
- `StateGraph` for defining node-based execution flows
- `MessagesState` or custom state classes for passing data between nodes
- Nodes are functions that take state and return state updates

### Configuration
- Environment variables loaded via `python-dotenv` in `app/config/settings.py`
- **Required environment variables:**
  - `OPENAI_API_KEY`: For OpenAI models
  - `GROQ_API_KEY`: For Groq models
- **Optional environment variables:**
  - `OPENAI_BASE_URL`: Custom OpenAI endpoint
- Settings managed through Pydantic models

### Schemas and Tools
- **Schemas** (`app/schemas/`): Pydantic models for data validation
  - `ExpenseData`: Expense record structure
  - `ExpenseAgentAction`: Agent action types with data
- **Tools** (`app/tools/`): LangChain tools decorated with `@tool`
  - Tools make API calls to external services (e.g., expense management API)

## Key Patterns

### Adding a New Agent
1. Create agent class in `app/agents/` inheriting from `BaseAgent`
2. Implement `run(self, state)` method
3. Use `self.call_llm(prompt, config)` for LLM calls
4. Return state dictionary with results

### Adding a New Workflow
1. Create workflow file in `app/workflow/`
2. Define state class (inherit from `MessagesState` or create custom)
3. Create `StateGraph`, add nodes, define edges
4. Compile with `app = graph.compile()`
5. Register in `langgraph.json` under "graphs"

### Adding a New LLM Provider
1. Create provider class in `app/llm/providers/` inheriting from `LLMClient`
2. Implement `invoke(prompt, config)` method using appropriate LangChain integration (e.g., `langchain-openai`, `langchain-groq`)
3. Update `LLMFactory.get_client()` to handle new provider
4. Add model mappings to `MODEL_REGISTRY`
5. Add API key configuration to `Settings` in `app/config/settings.py`
6. Install required LangChain integration package (e.g., `uv add langchain-groq`)

## Current State

The project is in active development with:
- Basic CLI interface in `main.py` (simple input loop)
- ExpenseAgent configured but workflow integration incomplete
- RouterAgent partially implemented
- LangGraph test UI available via `langgraph dev`
- Add to memory. Do not create comments in the code, unless it is EXTREMELY NECESSARY.