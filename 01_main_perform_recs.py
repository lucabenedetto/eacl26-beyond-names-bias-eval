import os
import pandas as pd

from utils import get_llm_response
from utils_keys import get_api_key_from_model
from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
    FRIEND_AS_STUDENT,
)
from prompts_friend_as_student import get_prompt_friend_as_student
from prompts_user_as_student import get_prompt_user_as_student
from prompts_llm_as_student import get_prompt_llm_as_student


def main(model, language, prompt_type, prompt_params_file, temperature=0.0, n_runs_per_prompt=1):
    # Each output file contains all the results for one temperature value and one model
    # Also, the script produces one file for the results with names and one for all the results without the names.

    if prompt_type not in {USER_AS_STUDENT, LLM_AS_STUDENT}:
        raise ValueError('Invalid prompt_type')

    api_key = get_api_key_from_model(model)

    out_df = pd.DataFrame(columns=['language', 'model', 'response', 'with_name', 'with_noun', 'with_adjective',
                                   'with_pronouns',
                                   'name', 'noun', 'adjective',
                                   'pronoun_0', 'pronoun_1', 'pronoun_2', 'pronoun_3', 'pronoun_4',
                                   'ending_id', 'n_uni_courses', 'prompt', 'temperature'])

    prompt_params_df = pd.read_csv(os.path.join('config', f'params_{prompt_params_file}_{language}.csv'))
    for row in prompt_params_df.itertuples():
        if prompt_type == USER_AS_STUDENT:
            prompt = get_prompt_user_as_student(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
        elif prompt_type == FRIEND_AS_STUDENT:
            prompt = get_prompt_friend_as_student(
                language=language,
                name=row.name,
                noun=row.noun,
                adjective=row.adjective,
                pronouns=(row.pronoun_0, row.pronoun_1, row.pronoun_2, row.pronoun_3, row.pronoun_4),
                n_uni_courses=row.n_uni_courses,
            )
        else:  # prompt_type == LLM_AS_STUDENT
            prompt = get_prompt_llm_as_student(language=language, name=row.name, noun=row.noun, adjective=row.adjective, n_uni_courses=row.n_uni_courses)
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
                'with_pronouns': [row.with_adjective],
                'name': [row.name],
                'noun': [row.noun],
                'adjective': [row.adjective],
                'pronoun_0': [row.pronoun_0],
                'pronoun_1': [row.pronoun_1],
                'pronoun_2': [row.pronoun_2],
                'pronoun_3': [row.pronoun_3],
                'pronoun_4': [row.pronoun_4],
                'ending_id': [row.ending_id],
                'n_uni_courses': [row.n_uni_courses],
                'prompt': [prompt],
                'temperature': [temperature],
            })
            if len(out_df) == 0:
                out_df = new_row_df.copy()
            else:
                out_df = pd.concat([out_df, new_row_df], ignore_index=True)

    folder_path = os.path.join('data', 'output', f'{prompt_type}', f'{language}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"[INFO] Created folder {folder_path}")
    else:
        print(f"[INFO] Folder already exists: {folder_path}")
    out_df.to_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'), index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = IT
    MODEL = GPT_4o_MINI
    N_RUNS_PER_PROMPT = 3
    TEMPERATURE = 0.0  # in [0.0, 0.3, 0.6]
    PROMPT_PARAMS_FILE = 'no_name'  # For experiments without names
    # PROMPT_PARAMS_FILE = 'with_names'  # For experiments with names
    PROMPT_TYPE = USER_AS_STUDENT  # or LLM_AS_STUDENT or FRIEND_AS_STUDENT

    main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE, n_runs_per_prompt=N_RUNS_PER_PROMPT)
