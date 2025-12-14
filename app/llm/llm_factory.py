from app.llm.providers.openai import OpenAIClient
# from app.llm.providers.ollama import OllamaClient

class LLMFactory:
    def get_client(self, provider: str):
        if provider == "openai":
            return OpenAIClient()
        if provider == "ollama":
            # return OllamaClient()
            pass
        raise ValueError(f"Provider not supported: {provider}")
