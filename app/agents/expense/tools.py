from langchain.tools import tool
from typing import List
from app.agents.expense.schemas import ExpenseData, ExpenseUpdate, Expense
from app.api.client import api_client
from app.api.exceptions import APIError


@tool
def create_expense(expense: ExpenseData) -> str:
    """Create a new expense record.

    Args:
        expense: ExpenseData object containing description, amount, category, and date
    """
    try:
        api_client.create_expense(expense.model_dump(mode="json"))
        return f"Expense '{expense.description}' for ${expense.amount} created successfully."
    except APIError as e:
        return f"Failed to create expense: {e.message}"


@tool
def list_expenses() -> str:
    """List all expense records."""
    try:
        expenses_data = api_client.list_expenses()

        if not expenses_data:
            return "No expenses found."

        expenses = [Expense(**exp) for exp in expenses_data]

        lines = [f"Found {len(expenses)} expense(s):"]
        for exp in expenses:
            date_str = exp.date.strftime("%Y-%m-%d")
            lines.append(
                f"  • [{exp.id}] {exp.description}: ${exp.amount} ({exp.category.value}) on {date_str}"
            )

        return "\n".join(lines)
    except APIError as e:
        return f"Failed to list expenses: {e.message}"
    except Exception as e:
        return f"Failed to parse expenses: {str(e)}"


@tool
def update_expense(expense_id: str, updates: ExpenseUpdate) -> str:
    """Update an existing expense record.

    Args:
        expense_id: ID of the expense to update
        updates: ExpenseUpdate object with optional description, amount, category, and date
    """
    try:
        api_client.update_expense(
            expense_id, updates.model_dump(exclude_none=True, mode="json")
        )
        return f"Expense {expense_id} updated successfully."
    except APIError as e:
        if e.status_code == 404:
            return f"Expense {expense_id} not found."
        return f"Failed to update expense: {e.message}"


@tool
def delete_expense(expense_id: str) -> str:
    """Delete an expense record.

    Args:
        expense_id: ID of the expense to delete
    """
    try:
        api_client.delete_expense(expense_id)
        return f"Expense {expense_id} deleted successfully."
    except APIError as e:
        if e.status_code == 404:
            return f"Expense {expense_id} not found."
        return f"Failed to delete expense: {e.message}"
