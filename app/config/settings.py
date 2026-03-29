from pydantic import BaseModel, model_validator
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_base_url: str | None = os.getenv("OPENAI_BASE_URL")
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    cashflow_api_url: str = os.getenv("CASHFLOW_API_URL")
    telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")

    @model_validator(mode="after")
    def validate_at_least_one_provider(self) -> "Settings":
        """Validate that at least one LLM provider API key is configured."""
        if not self.openai_api_key and not self.groq_api_key:
            raise ValueError(
                "At least one LLM provider API key must be set. "
                "Please set OPENAI_API_KEY or GROQ_API_KEY in your .env file."
            )
        return self
    
    @model_validator(mode="after")
    def validate_cashflow_api_url(self) -> "Settings":
        """Validate that the cashflow API URL is set."""
        if not self.cashflow_api_url:
            raise ValueError(
                "CASHFLOW_API_URL is not set. "
                "Please set it in your .env file to connect to the Cashflow API."
            )
        return self

    def validate_provider_key(self, provider: str) -> None:
        """Validate that the API key for a specific provider is configured.

        Args:
            provider: The provider name (openai, groq, ollama)

        Raises:
            ValueError: If the required API key is not set
        """
        if provider == "openai" and not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set. "
                "Please set it in your .env file to use OpenAI models."
            )
        elif provider == "groq" and not self.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Please set it in your .env file to use Groq models."
            )


settings = Settings()
