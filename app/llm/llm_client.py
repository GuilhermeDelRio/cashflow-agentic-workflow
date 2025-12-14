from abc import ABC, abstractmethod
from app.llm.llm_config import LLMConfig

class LLMClient(ABC):
    @abstractmethod
    def invoke(self, prompt: str, config: LLMConfig) -> str:
        """Invoke the LLM with the given prompt and configuration.

        Args:
            prompt (str): The input prompt to send to the LLM.
            config (LLMConfig): Configuration parameters for the LLM.

        Returns:
            str: The response from the LLM.
        """
        pass
