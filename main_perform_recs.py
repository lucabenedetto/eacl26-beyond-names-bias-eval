import pandas as pd

from utils import get_llm_response
from utils_keys import get_api_key_from_model
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5,
    GEMINI_1_5_FLASH_8B,
)
from prompts_user_as_student import get_prompt


def main(model, language, prompt_params_file, temperature=0.0, n_runs_per_prompt=1):
    # Each output file contains all the results for one temperature value and one model
    # Also, the script produces one file for the results with names and one for all the results without the names.

    api_key = get_api_key_from_model(model)

    out_df = pd.DataFrame(columns=['language', 'model', 'response', 'with_name', 'with_noun', 'with_adjective',
                                   'name', 'noun', 'adjective', 'ending_id', 'n_uni_courses', 'prompt', 'temperature'])

    prompt_params_df = pd.read_csv(f'params_{prompt_params_file}.csv')
    for row in prompt_params_df.itertuples():
        prompt = get_prompt(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
        print(f"[INFO] {prompt}")
        for _ in range(n_runs_per_prompt):
            response = get_llm_response(api_key, model, prompt, temperature)
            new_row_df = pd.DataFrame({
                'language': [language],
                'model': [model],
                'response': [response],
                'with_name': [row.with_name],
                'with_noun': [row.with_noun],
                'with_adjective': [row.with_adjective],
                'name': [row.name],
                'noun': [row.noun],
                'adjective': [row.adjective],
                'ending_id': [row.ending_id],
                'n_uni_courses': [row.n_uni_courses],
                'prompt': [prompt],
                'temperature': [temperature],
            })
            if len(out_df) == 0:
                out_df = new_row_df.copy()
            else:
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)

    out_df.to_csv(f'data/output/responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv', index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = IT
    MODEL = GPT_4o_MINI
    N_RUNS_PER_PROMPT = 1
    TEMPERATURE = 0.0
    # PROMPT_PARAMS_FILE = 'no_name'  # For experiments without names
    PROMPT_PARAMS_FILE = 'with_names'  # For experiments with names

    for TEMPERATURE in [0.3]:
        main(MODEL, LANGUAGE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE, n_runs_per_prompt=N_RUNS_PER_PROMPT)
