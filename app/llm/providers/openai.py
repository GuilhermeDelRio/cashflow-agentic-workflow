from langchain_openai import ChatOpenAI
from app.llm.llm_client import LLMClient
from app.llm.llm_config import LLMConfig
from app.config.settings import settings

class OpenAIClient(LLMClient):
    def invoke(self, prompt: str, config: LLMConfig) -> str:
        llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        return llm.invoke(prompt).content
