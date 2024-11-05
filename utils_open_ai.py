import openai
from retry import retry


@retry(tries=5, max_delay=60)
def get_openai_response(
        api_key: str,
        system_context: str = '',
        user_prompt: str = '',
        temperature=0,
        model=None,
) -> str:

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{'role': 'system', 'content': system_context},
                  {'role': 'user', 'content': user_prompt}],
        temperature=temperature,
        response_format={"type": 'text'}
    )
    response_content = response['choices'][0]['message']['content']
    return response_content
