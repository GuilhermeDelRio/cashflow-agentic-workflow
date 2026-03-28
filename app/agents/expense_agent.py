from app.agents.base_agent import BaseAgent
from app.llm.llm_config import LLMConfig
from app.schemas.expense import ExpenseAgentAction

class ExpenseAgent(BaseAgent):
    def run(self, state):
        
        prompt = f"""You are an Expense Management Agent. Your role is to help users manage their expenses by creating, reading, updating, or deleting expense records.

        Based on the user's request, determine which action to take:
        - CREATE: Add a new expense
        - READ: Retrieve expense information
        - UPDATE: Modify an existing expense
        - DELETE: Remove an expense

        User request: {state['input']}

        Analyze the request and respond with:
        1. The action (CREATE, READ, UPDATE, or DELETE)
        2. Relevant details needed for the API call
        3. A brief explanation of what will be done"""

        config = LLMConfig(
            model="gpt-4.1",
            temperature=0
        )

        result = self.call_llm(prompt, config)

        action = ExpenseAgentAction.model_validate_json(result)

        return {"result": result}