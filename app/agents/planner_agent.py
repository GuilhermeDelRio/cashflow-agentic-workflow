from app.agents.base_agent import BaseAgent
from app.llm.llm_config import LLMConfig

class PlannerAgent(BaseAgent):
    def run(self, state):
        prompt = f"Crie um plano para: {state['input']}"

        config = LLMConfig(
            model="gpt-4.1",
            temperature=0
        )

        plan = self.call_llm(prompt, config)

        return {"plan": plan}
