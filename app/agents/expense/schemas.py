from enum import Enum
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import date


class RecurrenceType(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ExpenseData(BaseModel):
    name: str
    value: float
    expense_date: date
    recurrence: Optional[RecurrenceType] = None
    installments_total: Optional[int] = None


class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    value: Optional[float] = None
    expense_date: Optional[date] = None


class ExpenseAgentAction(BaseModel):
    action: Literal[
        "create_expense",
        "update_expense",
        "delete_expense",
        "list_expenses",
        "ask_clarification",
        "none",
    ]
    data: Optional[ExpenseData] = None
