from langchain.tools import tool
from app.agents.expense.schemas import ExpenseData, ExpenseUpdate
from app.api.client import api_client
from app.api.exceptions import APIError


@tool
def create_expense(expense: ExpenseData) -> str:
    """Create a new expense record.

    Args:
        expense: ExpenseData object containing name, value, expense_date, and optional recurrence/installments_total
    """
    try:
        api_client.create_expense(expense.model_dump(mode="json"))
        return f"Expense '{expense.name}' for ${expense.value} created successfully."
    except APIError as e:
        return f"Failed to create expense: {e.message}"


@tool
def list_expenses() -> str:
    """List all expense records."""
    try:
        expenses = api_client.list_expenses()

        if not expenses:
            return "No expenses found."

        lines = [f"Found {len(expenses)} expense(s):"]
        for exp in expenses:
            recurrence = (
                f" (Recurring: {exp.get('recurrence_type')})"
                if exp.get("recurrence")
                else ""
            )
            lines.append(
                f"  • {exp['name']}: ${exp['value']} on {exp['expense_date']}{recurrence}"
            )

        return "\n".join(lines)
    except APIError as e:
        return f"Failed to list expenses: {e.message}"


@tool
def update_expense(expense_id: int, updates: ExpenseUpdate) -> str:
    """Update an existing expense record.

    Args:
        expense_id: ID of the expense to update
        updates: ExpenseUpdate object with optional name, value, and expense_date
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
def delete_expense(expense_id: int) -> str:
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
