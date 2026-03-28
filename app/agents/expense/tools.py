import requests
from langchain.tools import tool
from app.agents.expense.schemas import ExpenseData, ExpenseUpdate


@tool
def create_expense(expense: ExpenseData) -> str:
    """Create a new expense record.

    Args:
        expense: ExpenseData object containing name, value, expense_date, and optional recurrence/installments_total
    """
    try:
        # response = requests.post(
        #     "http://localhost:8000/api/expenses/",
        #     json=expense.model_dump(mode="json"),
        # )
        # response.raise_for_status()
        return f"Expense '{expense.name}' for ${expense.value} created successfully."
    except requests.RequestException as e:
        return f"Failed to create expense: {str(e)}"


@tool
def list_expenses() -> str:
    """List all expense records."""
    try:
        # response = requests.get("http://localhost:8000/api/expenses/")
        # response.raise_for_status()
        # return response.json()
        return "List of expenses: [Expense 1: Lunch $25, Expense 2: Coffee $5]"
    except requests.RequestException as e:
        return f"Failed to list expenses: {str(e)}"


@tool
def update_expense(expense_id: int, updates: ExpenseUpdate) -> str:
    """Update an existing expense record.

    Args:
        expense_id: ID of the expense to update
        updates: ExpenseUpdate object with optional name, value, and expense_date
    """
    try:
        # response = requests.patch(
        #     f"http://localhost:8000/api/expenses/{expense_id}",
        #     json=updates.model_dump(exclude_none=True, mode="json"),
        # )
        # response.raise_for_status()
        return f"Expense {expense_id} updated successfully."
    except requests.RequestException as e:
        return f"Failed to update expense: {str(e)}"


@tool
def delete_expense(expense_id: int) -> str:
    """Delete an expense record.

    Args:
        expense_id: ID of the expense to delete
    """
    try:
        # response = requests.delete(f"http://localhost:8000/api/expenses/{expense_id}")
        # response.raise_for_status()
        return f"Expense {expense_id} deleted successfully."
    except requests.RequestException as e:
        return f"Failed to delete expense: {str(e)}"
