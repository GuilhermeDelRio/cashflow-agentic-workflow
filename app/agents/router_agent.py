from app.agents.base_agent import BaseAgent
from app.llm.llm_config import LLMConfig

class RouterAgent(BaseAgent):
    def run(self, state):
        # prompt = f"Crie um plano para: {state['input']}"
        
        prompt = """
        You are a router agent. Based on the user's input, decide whether to route the request to the PlannerAgent or another specialized agent.
        """

        config = LLMConfig(
            model="gpt-4.1",
            temperature=0
        )

        plan = self.call_llm(prompt, config)

        return {"plan": plan}
