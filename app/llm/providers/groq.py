from langchain_groq import ChatGroq
from app.llm.llm_client import LLMClient
from app.llm.llm_config import LLMConfig
from app.config.settings import settings

class GroqClient(LLMClient):
    def invoke(self, prompt: str, config: LLMConfig) -> str:
        settings.validate_provider_key("groq")

        llm = ChatGroq(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=settings.groq_api_key,
        )
        return llm.invoke(prompt).content
