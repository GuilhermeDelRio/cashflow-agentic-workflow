# from langchain_community.chat_models import ChatOllama
# from app.llm.base import LLMClient
# from app.llm.config import LLMConfig

# class OllamaClient(LLMClient):
#     def invoke(self, prompt: str, config: LLMConfig) -> str:
#         llm = ChatOllama(
#             model=config.model,
#             temperature=config.temperature
#         )
#         return llm.invoke(prompt).content
