import json
from constants import (
    OPENAI_MODEL_TO_API_NAME,
    ANTHROPIC_MODEL_TO_API_NAME,
    GOOGLE_MODEL_TO_API_NAME,
    GROK_MODEL_TO_API_NAME,
)


def get_api_key_from_model(model):
    if model in OPENAI_MODEL_TO_API_NAME:
        path = '/home/luca/.keys/openai_key.json'
    elif model in ANTHROPIC_MODEL_TO_API_NAME:
        path = '/home/luca/.keys/anthropic_key.json'
    elif model in GOOGLE_MODEL_TO_API_NAME:
        path = '/home/luca/.keys/google_ai_api_key.json'
    elif model in GROK_MODEL_TO_API_NAME:
        path = '/home/luca/.keys/grok_key.json'
    else:
        raise ValueError(f"Model {model} not found")
    with open(path, 'r') as f:
        data = json.load(f)
        return data['key']
