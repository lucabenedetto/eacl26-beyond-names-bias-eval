import os
import pandas as pd

from constants import (
    IT, FR, EN,
    GPT_3_5, GPT_4o_MINI,
    CLAUDE_3_5_SONNET, CLAUDE_3_5_HAIKU,
    GEMINI_1_5_FLASH_8B, GEMINI_1_5_FLASH,
    USER_AS_STUDENT, LLM_AS_STUDENT,
)
from utils_parsing import parse_llm_response


def main(model, language, prompt_type, prompt_params_file, temperature=0.0):
    # Dataframe with the LLM responses.
    df = pd.read_csv(os.path.join('data', 'output', f'{prompt_type}', f'{language}',
                                  f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'))

    n_courses = df['n_uni_courses'].max()
    if df['n_uni_courses'].nunique() != 1:
        # The script should work when 'n_uni_courses' is not constant across the dataframe, but it has not been tested.
        print("[WARNING]: different values for 'n_uni_courses' in the dataframe.")

    # dataframe with the recommended courses.
    out_df = pd.DataFrame(columns=[f'rec_{idx}' for idx in range(n_courses)])

    for response, local_n_courses in df[['response', 'n_uni_courses']].values:
        # Parse the LLM response, get the recommended courses, and add the new row to the output dataframe.
        parsed_response = parse_llm_response(response, model=model)
        if parsed_response is None:
            parsed_response = ['NONE'] * n_courses
        if len(parsed_response) != local_n_courses:
            # Unsure about this. I now accept the first {n_courses} recommendations (or None if < n_courses)
            if len(parsed_response) > local_n_courses:
                print(f"Recommended more than {local_n_courses} items ({len(parsed_response)}). Complete list:")
                print(parsed_response)
                parsed_response = parsed_response[:local_n_courses]
                print(f"After filtering, keeping only the following {len(parsed_response)} items:")
                print(parsed_response)
            else:
                parsed_response = ['NONE'] * n_courses

        dict_new_row = {f'rec_{idx}': [item] for idx, item in enumerate(parsed_response)}

        # This can only happen if df['n_uni_courses'].nunique() != 1:
        if len(parsed_response) != n_courses:
            for idx in range(len(parsed_response), n_courses):
                dict_new_row[f'rec_{idx}'] = ['NONE']

        new_row_df = pd.DataFrame(dict_new_row)

        if len(out_df) == 0:
            out_df = new_row_df.copy()
        else:
            out_df = pd.concat([out_df, new_row_df], ignore_index=True)

    course_set = set(out_df[f'rec_0'].values)
    for idx in range(1, n_courses):
        course_set = course_set.union(set(out_df[f'rec_{idx}'].values))
    print("Complete list of courses recommended at least once:")
    print(sorted(list(course_set)))

    folder_path = os.path.join('data', 'processed_output', f'{prompt_type}', f'{language}')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"[INFO] Created folder {folder_path}")
    else:
        print(f"[INFO] Folder already exists: {folder_path}")
    print("\n")

    for idx in range(n_courses):
        df[f'rec_{idx}'] = out_df[f'rec_{idx}']

    df.to_csv(os.path.join(folder_path, f'responses_{model}_{language}_{prompt_params_file}_temp_{temperature}.csv'), index=False)


if __name__ == '__main__':
    # Params to set:
    LANGUAGE = IT
    MODEL = GEMINI_1_5_FLASH_8B

    for PROMPT_PARAMS_FILE in ['with_names', 'no_name']:
        for PROMPT_TYPE in [USER_AS_STUDENT, LLM_AS_STUDENT]:
            for TEMPERATURE in [0.0, 0.3, 0.6]:
                print(f"[INFO] Doing Model {MODEL} | Language {IT} | Temperature {TEMPERATURE} | Prompt type {PROMPT_TYPE} | Prompt params file {PROMPT_PARAMS_FILE}.")
                main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE)

    # PROMPT_PARAMS_FILE = 'with_names'
    # PROMPT_TYPE = LLM_AS_STUDENT
    # TEMPERATURE = 0.6
    # print(f"[INFO] Doing Model {MODEL} | Language {IT} | Temperature {TEMPERATURE} | Prompt type {PROMPT_TYPE} | Prompt params file {PROMPT_PARAMS_FILE}.")
    # main(MODEL, LANGUAGE, PROMPT_TYPE, PROMPT_PARAMS_FILE, temperature=TEMPERATURE)
