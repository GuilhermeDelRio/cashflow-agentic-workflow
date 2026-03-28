import requests
from langchain.tools import tool
from app.schemas.expense import ExpenseData


@tool
def create_expense(data: ExpenseData) -> str:
    """CREATE a new expense record using the provided data."""
    try:
        response = requests.post(
            "http://localhost:8000api/expenses/",
            json=data.model_dump(),
        )
        response.raise_for_status()
        return "Expense created successfully."
    except requests.RequestException as e:
        return f"Failed to create expense: {str(e)}"
