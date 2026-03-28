from pydantic import BaseModel, field_validator

class LLMConfig(BaseModel):
    model: str
    temperature: float = 0
    max_tokens: int | None = None

    @field_validator("model")
    @classmethod
    def validate_model_in_registry(cls, v: str) -> str:
        """Validate that the model exists in the MODEL_REGISTRY.

        Args:
            v: The model name to validate

        Returns:
            The validated model name

        Raises:
            ValueError: If the model is not found in MODEL_REGISTRY
        """
        from app.llm.registry import MODEL_REGISTRY

        if v not in MODEL_REGISTRY:
            available_models = ", ".join(sorted(MODEL_REGISTRY.keys()))
            raise ValueError(
                f"Model '{v}' is not registered in MODEL_REGISTRY. "
                f"Available models: {available_models}"
            )
        return v
