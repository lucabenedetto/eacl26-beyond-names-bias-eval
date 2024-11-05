from utils_anthropic import get_anthropic_response
from utils_open_ai import get_openai_response
from constants import (
    OPENAI_MODEL_TO_API_NAME,
    ANTHROPIC_MODEL_TO_API_NAME,
)

def get_llm_response(api_key, model, prompt, temperature):
    if model in OPENAI_MODEL_TO_API_NAME:
        try:
            response = get_openai_response(
                api_key=api_key,
                system_context='',
                user_prompt=prompt,
                model=OPENAI_MODEL_TO_API_NAME[model],
                temperature=temperature,
            )
        except Exception as e:
            print(e)
            response = "{'index': -9, 'text': 'None'}"  # this if the GPT model did not produce a response
    elif model in ANTHROPIC_MODEL_TO_API_NAME:
        try:
            response = get_anthropic_response(
                api_key=api_key,
                system_context='',
                user_prompt=prompt,
                model=ANTHROPIC_MODEL_TO_API_NAME[model],
                temperature=temperature,
            )
        except Exception as e:
            print(e)
            response = "{'index': -9, 'text': 'None'}"  # this if the model did not produce a response
    else:
        raise ValueError(f"Model {model} not found")
    return response
