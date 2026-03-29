from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Literal
import datetime as dt


class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"


# class RecurrenceType(str, Enum):
#     MONTHLY = "monthly"
#     YEARLY = "yearly"


class ExpenseData(BaseModel):
    description: str
    amount: float
    category: Category
    date: dt.datetime


class Expense(BaseModel):
    id: str = Field(..., json_schema_extra={"json": "id"})
    description: str = Field(..., json_schema_extra={"json": "description"})
    amount: float = Field(..., json_schema_extra={"json": "amount"})
    category: Category = Field(..., json_schema_extra={"json": "category"})
    date: dt.datetime = Field(..., json_schema_extra={"json": "date"})
    created_at: dt.datetime = Field(..., json_schema_extra={"json": "created_at"})
    updated_at: dt.datetime = Field(..., json_schema_extra={"json": "updated_at"})


class ExpenseUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[Category] = None
    date: Optional[dt.datetime] = None


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
