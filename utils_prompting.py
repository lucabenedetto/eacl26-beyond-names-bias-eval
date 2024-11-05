from constants import NO_NAME
from prompts import *


def get_list_prompts_from_id(prompt_id):
    if prompt_id == ID_001:
        return PROMPTS_ID_001
    if prompt_id == ID_002:
        return PROMPTS_ID_002
    raise ValueError(f"Unknown prompt_id {prompt_id}")


def get_prompt_from_name_language_prompt_id_and_version(name, language, prompt_id, prompt_version):
    prompt_dict = get_list_prompts_from_id(prompt_id)
    if name != NO_NAME:
        key = f'{language}_{prompt_version}'
        return prompt_dict[key][0] + name + prompt_dict[key][1]
    else:
        key = f'{language}_{prompt_version}_{name}'
        return prompt_dict[key][0]
