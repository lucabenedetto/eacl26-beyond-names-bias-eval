import google.generativeai as genai
from retry import retry


@retry(tries=5, max_delay=60)
def get_google_response(
        api_key: str,
        system_context: str = None,
        user_prompt: str = '',
        temperature=0,
        model=None,
) -> str:
    # TODO: Possibly move this outside if I don't want to always reconfigure it.
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name=model, system_instruction=system_context)
    response = model.generate_content(
        user_prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=1000,  # TODO set as param
            temperature=temperature,
        )
    )
    response_content = response.text
    return response_content
