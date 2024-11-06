import anthropic
from retry import retry
from constants import GROK_MODEL_TO_API_NAME


@retry(tries=5, max_delay=60)
def get_anthropic_response(
        api_key: str,
        system_context: str = '',
        user_prompt: str = '',
        temperature=0,
        model=None,
) -> str:
    if model in GROK_MODEL_TO_API_NAME:
        client = anthropic.Anthropic(api_key=api_key, base_url="https://api.x.ai")
    else:
        client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,  #"claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=temperature,
        system=system_context,
        messages=[{"role": "user", "content": [{"type": "text", "text": user_prompt}]}]
    )
    response_content = response.content[0].text
    return response_content
