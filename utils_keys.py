import os
from constants import (
    OPENAI_MODEL_TO_API_NAME,
    ANTHROPIC_MODEL_TO_API_NAME,
    GOOGLE_MODEL_TO_API_NAME,
)


def get_api_key_from_model(model):
    if model in OPENAI_MODEL_TO_API_NAME:
        key_name = 'OPENAI_KEY'
    elif model in ANTHROPIC_MODEL_TO_API_NAME:
        key_name = 'AWS_BEARER_TOKEN_BEDROCK'
    elif model in GOOGLE_MODEL_TO_API_NAME:
        key_name = 'GOOGLE_AI_KEY'
    else:
        raise ValueError(f"Model {model} not found")
    api_key = os.environ.get(key_name)

    if not api_key:
        raise ValueError(f"{key_name} is not set in environment variables!")

    return api_key
