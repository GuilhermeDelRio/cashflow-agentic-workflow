from pydantic import BaseModel

class LLMConfig(BaseModel):
    model: str
    temperature: float = 0
    max_tokens: int | None = None
