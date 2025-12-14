from app.llm.llm_factory import LLMFactory
from app.llm.llm_config import LLMConfig
from app.llm.registry import MODEL_REGISTRY

class BaseAgent:
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory

    def call_llm(self, prompt: str, config: LLMConfig) -> str:
        provider = MODEL_REGISTRY[config.model]
        client = self.llm_factory.get_client(provider)
        return client.invoke(prompt, config)
