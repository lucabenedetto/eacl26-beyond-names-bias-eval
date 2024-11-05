import pandas as pd

from utils import get_llm_response
from utils_keys import get_api_key_from_model
from utils_prompting import get_prompt_from_name_language_prompt_id_and_version
from constants import (
    NAMES_F,
    NAMES_M,
    NAMES_F_IT,
    NAMES_F_FR,
    NAMES_M_IT,
    NAMES_M_FR,
    NO_NAME,
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5,
    GEMINI_1_5_FLASH_8B,
)
from prompts import (
    ID_001,
    ID_002,
)


def main(list_names, language, prompt_id, prompt_version, model, temperature=0.0, n_runs_per_name=1):
    api_key = get_api_key_from_model(model)

    out_df = pd.DataFrame(columns=['language', 'model', 'prompt_id', 'prompt_version', 'name', 'temperature', 'response', 'prompt'])
    for name in list_names:
        prompt = get_prompt_from_name_language_prompt_id_and_version(name, language, prompt_id, prompt_version)
        print(f"[INFO] {prompt}")
        for _ in range(n_runs_per_name):
            response = get_llm_response(api_key, model, prompt, temperature)
            new_row_df = pd.DataFrame({'language': [language], 'model': [model], 'prompt_id': [prompt_id],
                                       'prompt_version': [prompt_version], 'name': [name], 'temperature': [temperature],
                                       'response': [response], 'prompt': [prompt]})
            out_df = pd.concat([out_df, new_row_df], ignore_index=True)
    out_df.to_csv(f'data/output/responses_{model}_{language}_{prompt_id}_{prompt_version}_temp_{temperature}.csv', index=False)


# LANGUAGE = FR
# PROMPT_ID = ID_001
MODEL = CLAUDE_3_5
# TEMPERATURE = 0
N_RUNS_PER_NAME = 5

if __name__ == '__main__':
    for PROMPT_ID in [ID_001, ID_002]:
    # for PROMPT_ID in [ID_001]:
    #     main([NO_NAME], IT, PROMPT_ID, 'f', CLAUDE_3_5, TEMPERATURE, 1)
        for TEMPERATURE in [0.0, 0.3, 0.6]:
            main(NAMES_F_IT + [NO_NAME], IT, PROMPT_ID, 'f', MODEL, TEMPERATURE, N_RUNS_PER_NAME)
            main(NAMES_M_IT + [NO_NAME], IT, PROMPT_ID, 'm', MODEL, TEMPERATURE, N_RUNS_PER_NAME)
            main(NAMES_F_FR + [NO_NAME], FR, PROMPT_ID, 'f', MODEL, TEMPERATURE, N_RUNS_PER_NAME)
            main(NAMES_M_FR + [NO_NAME], FR, PROMPT_ID, 'm', MODEL, TEMPERATURE, N_RUNS_PER_NAME)
